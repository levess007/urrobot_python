#!/bin/bash

#docker build -f base.dockerfile -t robot_base .

docker build -f control.dockerfile -t control .

docker tag control localhost:5000/control
