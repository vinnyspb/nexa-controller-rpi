import ConfigParser


class Config:
    def __init__(self, file_name='controller_config.ini'):
        self.RASPBERRY_PI_DATA_PIN = None
        self.TRANSMITTER_CODES = None
        self.EARLIEST_ENABLE_HOUR = None
        self.EARLIEST_ENABLE_MINUTE = None
        self.LATEST_DISABLE_HOUR = None
        self.LATEST_DISABLE_MINUTE = None
        self.ROUTER_HOST = None
        self.ROUTER_USERNAME = None
        self.ROUTER_PASSWORD = None
        self.MONITORED_MAC_ADRESSES = None
        self.KODI_ADDR = None
        self.DATADOG_API_KEY = None
        self.DATATOG_METRIC_NAME = None
        self.DATADOG_HOST_NAME = None
        self.DATADOG_ON_VALUE = None
        self.DATADOG_OFF_VALUE = None

        self.read_config(file_name)

    def read_config(self, file_name):
        config = ConfigParser.ConfigParser()
        read_files = config.read(file_name)
        if len(read_files) != 1:
            raise RuntimeError("Can't read {}".format(file_name))

        self.RASPBERRY_PI_DATA_PIN = int(config.get('HARDWARE', 'RASPBERRY_PI_DATA_PIN'))
        self.TRANSMITTER_CODES = [int(code) for code in config.get('HARDWARE', 'TRANSMITTER_CODES').split(',')]
        self.EARLIEST_ENABLE_HOUR = int(config.get('TIME', 'EARLIEST_ENABLE_HOUR'))
        self.EARLIEST_ENABLE_MINUTE = int(config.get('TIME', 'EARLIEST_ENABLE_MINUTE'))
        self.LATEST_DISABLE_HOUR = int(config.get('TIME', 'LATEST_DISABLE_HOUR'))
        self.LATEST_DISABLE_MINUTE = int(config.get('TIME', 'LATEST_DISABLE_MINUTE'))
        self.ROUTER_HOST = config.get('ROUTER', 'ROUTER_HOST')
        self.ROUTER_USERNAME = config.get('ROUTER', 'ROUTER_USERNAME')
        self.ROUTER_PASSWORD = config.get('ROUTER', 'ROUTER_PASSWORD')
        self.MONITORED_MAC_ADRESSES = config.get('ROUTER', 'MONITORED_MAC_ADRESSES').split(',')
        self.KODI_ADDR = config.get('KODI', 'KODI_ADDR')
        self.DATADOG_API_KEY = config.get('DATADOG', 'DATADOG_API_KEY')
        self.DATATOG_METRIC_NAME = config.get('DATADOG', 'DATATOG_METRIC_NAME')
        self.DATADOG_HOST_NAME = config.get('DATADOG', 'DATADOG_HOST_NAME')
        self.DATADOG_ON_VALUE = config.get('DATADOG', 'DATADOG_ON_VALUE')
        self.DATADOG_OFF_VALUE = config.get('DATADOG', 'DATADOG_OFF_VALUE')
