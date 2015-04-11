# nexa-controller-rpi

This small project was written in order to use Raspberry Pi as a central controller
for [Nexa](http://www.nexa.se/PE3-komplett-set-2.htm) remote-controlled electrical outlets.

## Configuration
Configuration can be done via `controller_config.py`

## Manual switch
To perfrm manual switch on/off (e.g. to pair RPi with the outlet), use:

`python manual_switch.py on|off data_pin_number transmitter_code`

## How to start
Start it using `./restart.sh`

Log will be written to `/var/log/nexa_controller.log`

## Modules
* **TimeController** module enables selected electric outlet between civil twilight
for your geographical location (fetched by public IP of Raspberry Pi gateway).


Many thanks to [this blog](http://tech.jolowe.se/home-automation-rf-protocols/) author
for a comprehensive Nexa protocol analysis

**freegeoip.net** public API is used to fetch geo position based on public IP address

**sunrise-sunset.org** public API is used to calculate twilight timings based on location
