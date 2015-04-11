#!/bin/sh

killall python
sleep 1
nohup python -u controller.py >/var/log/nexa_controller.log 2>&1 &

