FROM ubuntu:bionic

RUN apt update && \
    apt install -y --no-install-recommends python2.7-dev python3-dev python3-pip && \
    pip3 install requests


ENV PYTHONUNBUFFERED=TRUE
