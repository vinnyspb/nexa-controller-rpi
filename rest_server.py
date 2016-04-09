import web
from controller_config import Config
from switch_nexa import NexaSwitcher


class RestWindowSwitcher(object):
    def __init__(self, is_action_open):
        self._is_action_open = is_action_open

    def GET(self):
        switcher = NexaSwitcher(Config.RASPBERRY_PI_DATA_PIN, Config.TRANSMITTER_CODE)
        switcher.switch(self._is_action_open)
        return "OK"


class OpenWindow(RestWindowSwitcher):
    def __init__(self):
        super(OpenWindow, self).__init__(True)


class CloseWindow(RestWindowSwitcher):
    def __init__(self):
        super(CloseWindow, self).__init__(False)


urls = (
    '/open', 'OpenWindow',
    '/close', 'CloseWindow'
)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
