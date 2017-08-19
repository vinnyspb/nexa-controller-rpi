import unittest

from controller_config import Config


class ConfigTests(unittest.TestCase):
    def test_read_config(self):
        config = Config('../controller_config.ini.example')

        self.assertEqual(16, config.RASPBERRY_PI_DATA_PIN)
        self.assertIn(44756010, config.TRANSMITTER_CODES)
        self.assertIn(123456, config.TRANSMITTER_CODES)
        self.assertEqual(6, config.EARLIEST_ENABLE_HOUR)
        self.assertEqual(0, config.EARLIEST_ENABLE_MINUTE)
        self.assertEqual(22, config.LATEST_DISABLE_HOUR)
        self.assertEqual(0, config.LATEST_DISABLE_MINUTE)
        self.assertEqual("192.168.1.1", config.ROUTER_HOST)
        self.assertEqual("admin", config.ROUTER_USERNAME)
        self.assertEqual("admin", config.ROUTER_PASSWORD)
        self.assertIn("01:02:03:04:AA:BB", config.MONITORED_MAC_ADRESSES)
        self.assertIn("01:02:03:04:AA:CC", config.MONITORED_MAC_ADRESSES)
        self.assertIn("127.0.0.1:80", config.KODI_ADDR)
        self.assertIn("datadog_api_key", config.DATADOG_API_KEY)
        self.assertIn("metric.name", config.DATATOG_METRIC_NAME)
        self.assertIn("hostname_at_datadog", config.DATADOG_HOST_NAME)
        self.assertIn("1", config.DATADOG_ON_VALUE)
        self.assertIn("0", config.DATADOG_OFF_VALUE)
