#!/bin/bash

prio=${1:-0}

ip link add link enp8s0 name enp8s0.1 type vlan id 1 egress 0:$prio 1:$prio 2:$prio 3:$prio 4:$prio 5:$prio 6:$prio 7:$prio

#ip addr add 192.168.4.15/24 dev enp8s0.0

ifconfig enp8s0.1 up
