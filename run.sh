#!/bin/bash

docker stack rm robot-stack
docker stack deploy --compose-file swarm2.yaml robot-stack
