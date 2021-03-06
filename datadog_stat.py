import httplib
import time


class DataDogStat:
    def __init__(self, config):
        self._config = config

    def post_status(self, status):
        conn = httplib.HTTPSConnection("app.datadoghq.com", timeout=60)
        conn.request("GET", "/api/v1/validate?api_key=" + self._config.DATADOG_API_KEY)
        r1 = conn.getresponse()
        if r1.status != 200:
            raise Exception("Not 200 status in DataDog API login: " + str(r1.status))

        current_timestamp = int(time.time())
        if status:
            datadog_metric_value = self._config.DATADOG_ON_VALUE
        else:
            datadog_metric_value = self._config.DATADOG_OFF_VALUE

        headers = {"Content-type": "application/json"}
        post_data = '{ "series" : [{"metric":"' + self._config.DATATOG_METRIC_NAME + \
                    '", "points":[[' + str(current_timestamp) + \
                    ', ' + datadog_metric_value + ']], "type":"gauge", "host":"' + \
                    self._config.DATADOG_HOST_NAME + '", "tags\":[""]}]}'

        conn = httplib.HTTPSConnection("app.datadoghq.com", timeout=60)
        conn.request("POST", "/api/v1/series?api_key=" + self._config.DATADOG_API_KEY,
                     post_data,
                     headers)

        r1 = conn.getresponse()
        if r1.status != 202:
            raise Exception("Not 202 status in Datadog metric post: " + str(r1.status))

        return True
