#!/bin/bash

#docker build -f base.dockerfile -t robot_base .

docker build -f monitor.dockerfile -t monitor .

docker tag monitor localhost:5000/monitor

