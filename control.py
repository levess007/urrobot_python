#!/usr/bin/env python3

import socket
import requests
import json
import itertools
import time

NAME = 'CONTROL'

LOGIC_ADDR = ('localhost', 4321)
MONITOR_ADDR = ('localhost', 5432)
GRIPPER_IP = '10.6.6.11'
GRIPPER_TOLERANCE = 2  # mm
ROBOT_ADDR = ('10.6.6.10', 30002)
ROBOT_HOME = [0.35, -0.3, 0.132, 2.25, -2.25, 0]
SOLENOID = ('10.6.6.8', 7777)

class Logic:
    def __init__(self, addr):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect(addr)

    def get_task(self):
        print("{} - Querying task".format(NAME))
        self.server.send('get'.encode())
        recv_pos = self.server.recv(1024).decode().strip()
        task = json.loads(recv_pos)
        print("{} - Received task: {}".format(NAME, json.dumps(task, indent=4)))
        return task

class Monitor:
    def __init__(self, addr):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect(addr)

    def wait(self, pose):
        position = pose[:3]
        print("{} - Waiting for move completion".format(NAME))
        self.server.send(json.dumps(position).encode())
        recv = self.server.recv(1024).decode().strip()
        print("{} - Move completed".format(NAME))

class Gripper:
    def __init__(self, ip):
        self.ip = ip

    def wait(self, width):

        #actual_width = 1000  # outside range
        #request = 'http://{}/sensor_data'.format(self.ip)
        #while abs(actual_width - width) > GRIPPER_TOLERANCE:
        #    resp = requests.get(request)
        #    data = json.loads(resp.text)
        #    actual_width = data['devices'][0]['variable']['backpack']['width']
        time.sleep(0.3)
        print("{} - Gripper is set".format(NAME))

    def set_params(self, data):
        self.opened_mm = data['open']
        self.closed_mm = data['close']

    def set_width(self, width):
        print("{} - Setting gripper to {}mm".format(NAME, width))

        resp = requests.get('http://{}/api/dc/rg2ft/set_width/{}/40'.format(self.ip, width))
        if resp.status_code == 200:
            print("{} - OK".format(NAME))
            self.wait(width)
        else:
            raise Exception('Connection to gripper failed')

    def close(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes("MSG PLACEHOLDER", "utf-8"), SOLENOID)
        time.sleep(0.2) 
        self.set_width(self.closed_mm)
        

    def open(self):
        self.set_width(self.opened_mm)

class Robot:
    def __init__(self, addr):
        self.robot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.monitor = Monitor(MONITOR_ADDR)
        self.gripper = Gripper(GRIPPER_IP)
        self.payload = 0
        self.robot.connect(addr)
        self._move_home()

    def _create_move_command(self, move_type, pose, time=0):
        return '{}(get_inverse_kin(p{}),t={})\n'.format(move_type, json.dumps(pose),time)

    def _create_payload_command(self, payload):
        return 'set_payload({})\n'.format(payload)

    def _send_command(self, command):
        print("{} - Sending command - {}".format(NAME, command.strip()))
        self.robot.send(command.encode())

    def _move_home(self):
        command = self._create_move_command('movej', ROBOT_HOME, 2)
        self._send_command(command)
#        self.monitor.wait(ROBOT_HOME)
        time.sleep(3)

    def _move_above(self, data):
        pose = data['pose'].copy()
        pose[2] += data['lift_height']
        command = self._create_move_command('movej', pose, 1)
        self._send_command(command)
#        self.monitor.wait(pose)

    def _move_vertical(self, data, direction):
        if direction not in ['up', 'down']:
            raise Exception('Invalid parameter for direction - {}'.format(direction))

        pose = data['pose'].copy()
        if direction is 'up':
            pose[2] += data['lift_height']

        command = self._create_move_command('movel', pose, 0.5)
        self._send_command(command)
#        self.monitor.wait(pose)

    def _set_payload(self, payload):
        command = self._create_payload_command(payload)
        self._send_command(command)

    def setup_gripper(self, gripper_data):
        self.gripper.set_params(gripper_data)
        #self.gripper.open()
        self.payload = gripper_data['payload']


if __name__ == "__main__":
    logic = Logic(LOGIC_ADDR)
    robot = Robot(ROBOT_ADDR)

    while True:
        
        task = logic.get_task()

        robot.setup_gripper(task['gripper'])
        
        robot._move_above(task['from'])
        time.sleep(1)
        robot._move_vertical(task['from'], 'down')
        time.sleep(0.6)
        
        robot._set_payload(robot.payload)
        robot.gripper.close()
        
        robot._move_vertical(task['from'], 'up')
        time.sleep(0.6)
        
        robot._move_above(task['to'])
        time.sleep(1.05)
        robot._move_vertical(task['to'], 'down')
        time.sleep(0.6)
        
        robot._set_payload(0)
        robot.gripper.open()
        
        robot._move_vertical(task['to'], 'up')
        time.sleep(0.6)
