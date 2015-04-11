import sys
import time
sys.path.append("/storage/.kodi/addons/python.RPi.GPIO/lib")
import RPi.GPIO as GPIO

data_pin = 16 #gpio23

def sleep_T(T_num):
	time.sleep(T_num*250/1000000.0)

def send_physical_bit(pin, bit_value):
	if bit_value:
		GPIO.output(pin, True)
		sleep_T(1)
		GPIO.output(pin, False)
		sleep_T(1)
	else:
		GPIO.output(pin, True)
		sleep_T(1)
		GPIO.output(pin, False)
		sleep_T(5)

def send_bit(pin, bit_value):
	send_physical_bit(pin, bit_value)
	send_physical_bit(pin, not bit_value)

def send_sync(pin):
	GPIO.output(pin, True)
	sleep_T(1)
	GPIO.output(pin, False)
	sleep_T(10)

def send_pause(pin):
	GPIO.output(pin, True)
	sleep_T(1)
	GPIO.output(pin, False)
	sleep_T(40)

def send_on_off(pin, on_off):
	send_sync(pin)

	#transmitter code, choosed by fair random :)
	send_bit(pin, True)
	send_bit(pin, False)
	send_bit(pin, True)
	send_bit(pin, False)
	send_bit(pin, True)
	send_bit(pin, False)
	send_bit(pin, True)
	send_bit(pin, False)
	send_bit(pin, True)
	send_bit(pin, False)
	send_bit(pin, True)
	send_bit(pin, True)
	send_bit(pin, True)
	send_bit(pin, False)
	send_bit(pin, True)
	send_bit(pin, True)
	send_bit(pin, False)
	send_bit(pin, False)
	send_bit(pin, False)
	send_bit(pin, False)
	send_bit(pin, True)
	send_bit(pin, False)
	send_bit(pin, True)
	send_bit(pin, False)
	send_bit(pin, True)
	send_bit(pin, False)

	#group code
	send_bit(pin, True)

	#on/off bit, on = 0, off = 1
	send_bit(pin, not on_off)
	
	#Channel bits. Proove/Anslut = 00, Nexa = 11.
	send_bit(pin, True)
	send_bit(pin, True)

	# Unit bits. Device to be turned on or off.
	# Nexa Unit #1 = 11, #2 = 10, #3 = 01.
	send_bit(pin, True)
	send_bit(pin, True)
	
	send_pause(pin)

def switch_nexa(pin, on_off):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin, GPIO.OUT)
	for x in range(0, 5):
		send_on_off(pin, on_off)
	GPIO.cleanup()


if len(sys.argv) < 2:
    sys.exit('Usage: %s on|off' % sys.argv[0])

if sys.argv[1] == "on":
	switch_nexa(data_pin, True)
else:
	switch_nexa(data_pin, False)

