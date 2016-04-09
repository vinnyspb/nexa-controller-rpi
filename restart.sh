#!/bin/sh

sudo killall python
sleep 1
sudo su -c 'nohup python -u controller.py >/run/nexa_controller.log 2>&1 &'
sudo su -c 'nohup python -u rest_server.py >/run/nexa_rest_server.log 2>&1 &'
