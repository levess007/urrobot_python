#!/usr/bin/env python3

import socket
import requests
import json
import itertools
import time

NAME = 'CONTROL'

GRIPPER_IP = '10.6.6.11'
GRIPPER_TOLERANCE = 2  # mm
GRIPPER_CLOSED = 38 # mm
GRIPPER_OPEN = 52 # mm
PAYLOAD = 0.10 # kg
ROBOT_ADDR = ('10.6.6.10', 30002)
ROBOT_HOME = [0.355, -0.3, 0.132, 2.25, -2.25, 0]
SOLENOID = ('10.6.6.8', 7777)


class Gripper:
    def __init__(self, ip):
        self.ip = ip

    def wait(self, width):
        print("{} - Gripper is set".format(NAME))

    def set_width(self, width):
        print("{} - Setting gripper to {}mm".format(NAME, width))

        resp = requests.get('http://{}/api/dc/rg2ft/set_width/{}/40'.format(self.ip, width))
        if resp.status_code == 200:
            print("{} - OK".format(NAME))
            self.wait(width)
        else:
            raise Exception('Connection to gripper failed')

    def close(self):
        self.set_width(GRIPPER_CLOSED)
        

    def open(self):
        self.set_width(GRIPPER_OPEN)

class Robot:
    def __init__(self, addr):
        self.robot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gripper = Gripper(GRIPPER_IP)
        self.payload = 0
        self.robot.connect(addr)
        self._move_home()

    def close_gripper(self, width, force):
        self._send_command('rg_grip({},{})\n'.format(width,force))

    def _create_move_command(self, move_type, pose, time=0):
        return '{}(get_inverse_kin(p{}),t={})\n'.format(move_type, json.dumps(pose),time)

    def _create_payload_command(self, payload):
        return 'set_payload({})\n'.format(payload)

    def _send_command(self, command):
        print("{} - Sending command - {}".format(NAME, command.strip()))
        self.robot.send(command.encode())

    def _move_home(self, timeToComplete=0):
        command = self._create_move_command('movej', ROBOT_HOME, timeToComplete)
        self._send_command(command)
        self.gripper.open()
        time.sleep(2)
    
    def _move(self, moveType, pose, timeToComplete=0):
        command = self._create_move_command(moveType, pose, timeToComplete)
        self._send_command(command)

    def _move_above(self, pose, timeToComplete=0):
        command = self._create_move_command('movej', pose, timeToComplete)
        self._send_command(command)

    def _move_vertical(self, pose, timeToComplete=0):
        command = self._create_move_command('movel', pose, timeToComplete)
        self._send_command(command)

    def _set_payload(self, payload):
        command = self._create_payload_command(payload)
        self._send_command(command)


if __name__ == "__main__":
    robot = Robot(ROBOT_ADDR)

    #robot.close_gripper(80,20)
    #time.sleep(5)

    while True:
        robot._move('movel',[0.413, -0.32, 0.05, 2.25, -2.25, 0], 1) # ELKAPAS POZICIO
        time.sleep(0.9)
        
        robot.gripper.close()
        #time.sleep(0.015) # solenoid utes commandtol a gripper set commandig eltelt ido
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes("MSG PLACEHOLDER", "utf-8"), SOLENOID)
        sock.close()
        
        time.sleep(0.3)

        robot._move('movel',[0.413, -0.12, 0.045, 2.25, -2.25, 0], 1) # VISSZARAKAS POZICIO
        time.sleep(1)
        robot.gripper.open()
        time.sleep(0.2)
