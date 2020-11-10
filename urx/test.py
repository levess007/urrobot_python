#!/usr/bin/env python2.7
import urx
import time
import sys
from urx.robotiq

rob = urx.Robot("10.6.6.10")
print "setup"
time.sleep(1)
print "Current tool pos: ", rob.getl()

