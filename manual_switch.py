import sys

from switch_nexa import NexaSwitcher

if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit('Usage: %s on|off data_pin_number transmitter_code' % sys.argv[0])

    switcher = NexaSwitcher(data_pin=int(sys.argv[2]), transmitter_code=int(sys.argv[3]))
    if sys.argv[1] == "on":
        switcher.switch(True)
    else:
        switcher.switch(False)
