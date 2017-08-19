import logging
import os
import sched
import sys
import time

from controller_config import Config
from datadog_stat import DataDogStat
from kodi_play_pause import KodiPlayPause
from presence_controller import PresenceController
from switch_nexa import NexaSwitcher
from time_controller import TimeController


def dispatch_all_controllers(sc, config, controllers, global_status):
    try:
        new_status = True
        for controller in controllers:
            if not controller.dispatch():
                new_status = False
                break

        if global_status is None or global_status != new_status:
            kodi = None
            if config.KODI_ADDR is not None and len(config.KODI_ADDR) > 0:
                kodi = KodiPlayPause(config)
                kodi.pause()
                time.sleep(1)

            logging.info("Changing status from " + str(global_status) + " to " + str(new_status))
            os.nice(+40)
            for transmitter_code in config.TRANSMITTER_CODES:
                switcher = NexaSwitcher(config.RASPBERRY_PI_DATA_PIN, transmitter_code)
                switcher.switch(new_status)
                time.sleep(1)
            os.nice(-40)

            if kodi is not None:
                kodi.play()

            global_status = new_status

        if config.DATADOG_API_KEY is not None and len(config.DATADOG_API_KEY) > 0:
            datadog = DataDogStat(config)
            datadog.post_status(new_status)

    except Exception as e:
        logging.exception("Controller dispatch error")

    sc.enter(60, 1, dispatch_all_controllers, (sc, config, controllers, global_status))


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(message)s')

    global_status = None
    config = Config()
    controllers = [TimeController(config),
                   PresenceController(config.ROUTER_HOST, config.ROUTER_USERNAME,
                                      config.ROUTER_PASSWORD, config.MONITORED_MAC_ADRESSES)]
    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, dispatch_all_controllers, (s, config, controllers, global_status))
    s.run()


if __name__ == '__main__':
    main()
