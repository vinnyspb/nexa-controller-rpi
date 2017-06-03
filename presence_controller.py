import telnetlib
import time
from datetime import datetime


class PresenceController:
    def __init__(self, router_host, router_username, router_password, monitored_mac_addresses):
        self._router_host = router_host
        self._router_username = router_username
        self._router_password = router_password

        # dict MAC address -> last seen timestamp
        self._monitored_mac_addresses = dict(zip(monitored_mac_addresses,
                                                 [datetime.fromtimestamp(0)]*len(monitored_mac_addresses)))

    def _check_connected_devices(self):
        tn = telnetlib.Telnet(self._router_host)

        tn.read_until("login: ")
        tn.write(self._router_username + "\n")
        tn.read_until("Password: ")
        tn.write(self._router_password + "\n")

        tn.write("wl -i eth2 assoclist\n")
        tn.write("exit\n")

        response = tn.read_all()
        for device in self._monitored_mac_addresses.keys():
            if device in response:
                self._monitored_mac_addresses[device] = datetime.now()

    def dispatch(self):
        successful_result = False
        while not successful_result:
            try:
                self._check_connected_devices()
                successful_result = True
            except Exception as e:
                print str(e)
                print "Sleeping 60 seconds..."
                time.sleep(60)

        current_time = datetime.now()
        for device in self._monitored_mac_addresses.keys():
            time_diff = current_time - self._monitored_mac_addresses[device]
            if time_diff.total_seconds() < 5*60:
                return True

        print "PresenceController: No devices from the list are alive for the last 5 minutes, disabling:" +\
              str(self._monitored_mac_addresses)
        return False
