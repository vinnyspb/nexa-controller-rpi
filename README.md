# nexa-controller-rpi

This small project was written in order to use Raspberry Pi as a central controller
for [Nexa](http://www.nexa.se/PE3-komplett-set-2.htm) remote-controlled electrical outlets.

## Hardware
Besides Nexa electrical outlets itself and Raspberry Pi, you will need a 433 MHz transmitter module
for Rasberry Pi like [this one](http://www.kjell.com/sortiment/el/elektronik/fjarrstyrning/433-mhz-sandarmodul-p88901).

## Configuration
All tests were performed on Raspberry Pi with OpenELEC 5.0.8 installed.
RPi.GPIO python package is required. It may be tricky to install it using pip or easy_install on OpenELEC.
Use GUI add-ons download instead.

Configuration can be done via `controller_config.py`

## Manual switch
To perform manual switch on/off (e.g. to pair RPi with the outlet), use:

`python manual_switch.py on|off data_pin_number transmitter_code`

## How to start
Start it using `./restart.sh`

Log will be written to `/run/nexa_controller.log`

## Modules
* **TimeController** module enables selected electric outlet between sunrise and sunset
for your geographical location (fetched by public IP of Raspberry Pi gateway)
* **PresenceController** module allows to enable selected electric outlet only when
configured MAC addresses are connected to the local router (tested on ASUS RT-AC66U).


Many thanks to [this blog](http://tech.jolowe.se/home-automation-rf-protocols/) author
for a comprehensive Nexa protocol analysis

**freegeoip.net** public API is used to fetch geo position based on public IP address

**sunrise-sunset.org** public API is used to calculate twilight timings based on location
