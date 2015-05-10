import httplib
import json
import time
from controller_config import Config

class DataDogStat:
    def __init__(self):
        None

    def post_status(self, status):
        conn = httplib.HTTPSConnection("app.datadoghq.com")
        conn.request("GET", "/api/v1/validate?api_key=" + Config.DATADOG_API_KEY)
        r1 = conn.getresponse()
        if r1.status != 200:
            raise Exception("Not 200 status in DataDog API login: " + str(r1.status))

        current_timestamp = int(time.time())
        if status:
            datadog_metric_value = Config.DATADOG_ON_VALUE
        else:
            datadog_metric_value = Config.DATADOG_OFF_VALUE

        headers = {"Content-type": "application/json"}
        post_data = '{ "series" : [{"metric":"' + Config.DATATOG_METRIC_NAME +\
                     '", "points":[[' + str(current_timestamp) +\
                     ', ' + datadog_metric_value + ']], "type":"gauge", "host":"' +\
                     Config.DATADOG_HOST_NAME + '", "tags\":[""]}]}'

        conn = httplib.HTTPSConnection("app.datadoghq.com")
        conn.request("POST", "/api/v1/series?api_key=" + Config.DATADOG_API_KEY,
                     post_data,
                     headers)

        r1 = conn.getresponse()
        if r1.status != 202:
            raise Exception("Not 202 status in Datadog metric post: " + str(r1.status))

        return True
