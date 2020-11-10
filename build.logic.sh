#!/bin/bash

#docker build -f base.dockerfile -t robot_base .

docker build -f logic.dockerfile -t logic .

docker tag logic localhost:5000/logic
