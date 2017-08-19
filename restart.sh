#!/bin/sh

sudo killall python
sleep 1
sudo su -c 'nohup python -u controller.py >/run/nexa_controller.log 2>&1 &'
sudo su -c 'nohup python -u web_interface.py >/run/nexa_web_interface.log 2>&1 &'
