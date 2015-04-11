import httplib
import json
import time
from datetime import datetime, timedelta
from controller_config import Config

class TimeController:
    def __init__(self):
        self._current_date = None
        self._sunrise = None
        self._sunset = None
        self._fetch_location()

    def _fetch_location(self):
        conn = httplib.HTTPSConnection("freegeoip.net")
        conn.request("GET", "/json/")
        r1 = conn.getresponse()
        if r1.status != 200:
            return False

        data1 = r1.read()
        decoded_json = json.loads(data1)

        if decoded_json is None:
            return False

        self._latitude = decoded_json['latitude']
        self._longitude = decoded_json['longitude']
        print "Fetched device position: (" + str(self._latitude) + ", " + str(self._longitude) + ")"

    def decode_utc_time(self, date_str, time_str):
        t = datetime.strptime(date_str + ' ' + time_str, "%Y-%m-%d %I:%M:%S %p")

        tz_offset = -time.timezone
        local_time = time.localtime()
        if local_time.tm_isdst == 1:
            tz_offset += 3600

        res = t + timedelta(seconds=tz_offset)
        return res

    # I know that it could be calculated without using any external APIs
    # but those existing python packages that are already implemented
    # could not be easily installed into OpenELEC because of broken dependency install
    # system. And I'm too lazy to implement this maths on my own :)
    def get_sunrise_sunset(self, date_str):
        conn = httplib.HTTPConnection("api.sunrise-sunset.org")
        conn.request("GET", "/json?lat=" + str(self._latitude) + "&lng=" + str(self._longitude) + "&date=" + date_str)
        r1 = conn.getresponse()
        if r1.status != 200:
            return False

        data1 = r1.read()
        decoded_json = json.loads(data1)

        if decoded_json is None or decoded_json['status'] != "OK":
            return False

        self._sunrise = self.decode_utc_time(date_str, decoded_json['results']['sunrise'])
        self._sunset = self.decode_utc_time(date_str, decoded_json['results']['sunset'])

        return True

    def dispatch(self):
        current_time = datetime.now()
        current_date = current_time.strftime("%Y-%m-%d")
        if self._current_date is None or self._current_date != current_date:
            print "New date: " + current_date
            self._current_date = current_date

            self.get_sunrise_sunset(current_date)
            print "Today's sunrise: " + str(self._sunrise)
            print "Today's sunset: " + str(self._sunset)

            current_date = datetime.now()
            lower_bound = current_date.replace(hour=Config.EARLIEST_ENABLE_HOUR,
                                               minute=Config.EARLIEST_ENABLE_MINUTE,
                                               second=0)
            upper_bound = current_date.replace(hour=Config.LATEST_DISABLE_HOUR,
                                               minute=Config.LATEST_DISABLE_MINUTE,
                                               second=0)
            print "Lower bound: " + str(lower_bound)
            print "Upper bound: " + str(upper_bound)

            if self._sunrise < lower_bound:
                self._sunrise = lower_bound
                print "Sunrise is before lower bound, using lower bound"
            if self._sunset > upper_bound:
                self._sunset = upper_bound
                print "Sunset is after upper bound, using upper bound"

        return self._sunrise < current_time and current_time < self._sunset
