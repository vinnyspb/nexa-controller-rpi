import sys
import time
from switch_nexa import NexaSwitcher

if len(sys.argv) != 4:
    sys.exit('Usage: %s blink_N_times data_pin_number transmitter_code' % sys.argv[0])

times_to_blink = int(sys.argv[1])
switcher = NexaSwitcher(data_pin=int(sys.argv[2]), transmitter_code=int(sys.argv[3]))

for i in range(0, times_to_blink):
    switcher.switch(True)
    time.sleep(0.5)
    switcher.switch(False)
    time.sleep(0.5)

