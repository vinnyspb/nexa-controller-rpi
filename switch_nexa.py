import sys
import time
sys.path.append("/storage/.kodi/addons/python.RPi.GPIO/lib")
import RPi.GPIO as GPIO

class NexaSwitcher:
    def __init__(self, data_pin, transmitter_code):
        self._data_pin = data_pin
        self._transmitter_code = transmitter_code
        print "Created NexaSwitcher for data PIN #" + str(self._data_pin) + " and transmitter code: " +\
              str(self._transmitter_code)

    def sleep_T(self, T_num):
        time.sleep(T_num*250/1000000.0)

    def send_physical_bit(self, bit_value):
        if bit_value:
            GPIO.output(self._data_pin, True)
            self.sleep_T(1)
            GPIO.output(self._data_pin, False)
            self.sleep_T(1)
        else:
            GPIO.output(self._data_pin, True)
            self.sleep_T(1)
            GPIO.output(self._data_pin, False)
            self.sleep_T(5)

    def send_bit(self, bit_value):
        self.send_physical_bit(bit_value)
        self.send_physical_bit(not bit_value)

    def send_sync(self):
        GPIO.output(self._data_pin, True)
        self.sleep_T(1)
        GPIO.output(self._data_pin, False)
        self.sleep_T(10)

    def send_pause(self):
        GPIO.output(self._data_pin, True)
        self.sleep_T(1)
        GPIO.output(self._data_pin, False)
        self.sleep_T(40)

    def send_on_off(self, on_off):
        self.send_sync()

        #transmitter code
        binary_number_string = format(self._transmitter_code, '08b')
        for digit in binary_number_string:
            bit = digit == '1'
            self.send_bit(bit)

        #group code
        self.send_bit(True)

        #on/off bit, on = 0, off = 1
        self.send_bit(not on_off)

        #Channel bits. Proove/Anslut = 00, Nexa = 11.
        self.send_bit(True)
        self.send_bit(True)

        # Unit bits. Device to be turned on or off.
        # Nexa Unit #1 = 11, #2 = 10, #3 = 01.
        self.send_bit(True)
        self.send_bit(True)

        self.send_pause()

    def switch(self, on_off):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._data_pin, GPIO.OUT)
        for x in range(0, 5):
            self.send_on_off(on_off)

        # Send the signal one more time,
        # sometimes it happens not to be decoded correctly
        time.sleep(1)
        for x in range(0, 5):
            self.send_on_off(on_off)

	GPIO.output(self._data_pin, False) # Make sure that we do not leave PIN in 'on' state
        GPIO.cleanup()

