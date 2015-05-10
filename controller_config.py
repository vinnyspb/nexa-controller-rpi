class Config:
    # Raspberry Pi GPIO23
    RASPBERRY_PI_DATA_PIN = 16

    # You can choose your own transmitter code randomly
    TRANSMITTER_CODE = 44756010

    # Earliest enable time, regardless of sunrise EARLIEST_ENABLE_HOUR:EARLIEST_ENABLE_MINUTE local (24h format)
    EARLIEST_ENABLE_HOUR = 6
    EARLIEST_ENABLE_MINUTE = 0

    # Latest disable time, regardless of sunset LATEST_DISABLE_HOUR:LATEST_DISABLE_MINUTE local (24h format)
    LATEST_DISABLE_HOUR = 22
    LATEST_DISABLE_MINUTE = 0

    # Router web interface access settings to get connected devices on local network
    ROUTER_HOST = "192.168.1.1"
    ROUTER_URI = "/update_clients.asp"
    ROUTER_USERNAME = "admin"
    ROUTER_PASSWORD = "admin"

    # MAC addresses list that should be online locally to enable Nexa outlet
    MONITORED_MAC_ADRESSES = ["01:02:03:04:AA:BB", "01:02:03:04:AA:CC"]

    # Add suffix/prefix optionally to search with the MAC address on router web interface
    SEARCH_PREFIX_FOR_MAC = '["'
    SEARCH_SUFFIX_FOR_MAC = '", "Yes", "Yes"'

    # Datadog API settings (optional)
    DATADOG_API_KEY = "datadog_api_key"
    DATATOG_METRIC_NAME = "metric.name"
    DATADOG_HOST_NAME = "hostname_at_datadog"
    DATADOG_ON_VALUE = "1"
    DATADOG_OFF_VALUE = "0"
