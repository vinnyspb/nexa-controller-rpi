import httplib
import json
from controller_config import Config

class KodiPlayPause:
    def __init__(self):
        None

    def _switch_play_pause(self):
        conn = httplib.HTTPConnection(Config.KODI_ADDR)
        conn.request("POST", "/jsonrpc", '{"jsonrpc": "2.0", "method": "Player.PlayPause", "params": { "playerid": 1 }, "id": 1}')

        r1 = conn.getresponse()
        if r1.status != 200:
            raise Exception("Not 200 status in Kodi API: " + str(r1.status))

        data1 = r1.read()
        decoded_json = json.loads(data1)

        if 'result' in decoded_json:
            if 'speed' in decoded_json['result']:
                return decoded_json['result']['speed'] == 1

        return False

    def play(self):
        result = self._switch_play_pause()
        if not result:
            self._switch_play_pause()

    def pause(self):
        result = self._switch_play_pause()
        if result:
            self._switch_play_pause()
