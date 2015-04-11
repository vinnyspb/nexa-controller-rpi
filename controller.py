import sched
import time
import os
from datetime import datetime
from switch_nexa import NexaSwitcher
from time_controller import TimeController
from controller_config import Config

def dispatch_all_controllers(sc, controllers, global_status):
    new_status = True
    for controller in controllers:
        if not controller.dispatch():
            new_status = False
            break

    if global_status is None or global_status != new_status:
        print str(datetime.now()) + " Changing status from " + str(global_status) + " to " + str(new_status)
        os.nice(+40)
        switcher = NexaSwitcher(Config.RASPBERRY_PI_DATA_PIN, Config.TRANSMITTER_CODE)
        switcher.switch(new_status)
        os.nice(-40)
        global_status = new_status

    sc.enter(60, 1, dispatch_all_controllers, (sc,controllers,global_status))

global_status = None
controllers = [TimeController()]
s = sched.scheduler(time.time, time.sleep)
s.enter(1, 1, dispatch_all_controllers, (s,controllers,global_status))
s.run()
