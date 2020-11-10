#!/bin/bash
vconfig set_egress_map enp8s0.5 0 3  #robot
vconfig set_egress_map enp8s0.7 0 1  #gripper
vconfig set_egress_map enp8s0.4 0 2  #solenoid

#ip link set enp8s0.5 type vlan egress 0:7 1:7 2:7 3:7 4:7 5:7 6:7 7:7
