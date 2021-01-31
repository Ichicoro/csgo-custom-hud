from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json

from PyQt5.QtCore import QThread, pyqtSignal

from gsi import payloadparser, gamestate, provider


class GSIDaemon(QThread):
    _signal = pyqtSignal((int, int, str, int, int))
    def run(self):
        self._server = GSIServer(('localhost', 3001), 'caccamelone', RequestHandler, data_handler=lambda data: self.handler(data))
        self._server.serve_forever()

    def stop(self):
        self._server.shutdown()
        self._server.socket.close()
        self.wait()

    def handler(self, data):
        print(data.player.weapons)
        weapon_name: str = ""
        weapon_ammo_clip: int = 0
        weapon_clip_size: int = 0
        for weapon in data.player.weapons.values():
            if weapon["state"] == "active":
                weapon_name = weapon["name"]
                if weapon["type"] != "Knife":
                    weapon_ammo_clip = weapon["ammo_clip"]
                    weapon_clip_size = weapon["ammo_clip_max"]

        self._signal.emit(
            data.player.state.health,
            data.player.state.armor,
            weapon_name,
            weapon_ammo_clip,
            weapon_clip_size
        )


class GSIServer(HTTPServer):
    def __init__(self, server_address, token, RequestHandler, data_handler):
        super(GSIServer, self).__init__(server_address, RequestHandler)
        self.provider = provider.Provider()
        self.auth_token = token
        self.gamestatemanager = gamestate.GameStateManager()
        self.data_handler = data_handler

        # old super()

        # self.setup_log_file()
        self.payload_parser = payloadparser.PayloadParser()

    # def setup_log_file(self):
    #     self.log_file = logger.LogFile(time.asctime())

    def on_parsed_data(self):
        self.data_handler(data=self.gamestatemanager.gamestate)


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')

        payload = json.loads(body)
        # Ignore unauthenticated payloads
        if not self.authenticate_payload(payload):
            return None

        # self.server.log_file.log_event(time.asctime(), payload)
        self.server.payload_parser.parse_payload(payload, self.server.gamestatemanager)
        self.server.on_parsed_data()

        self.send_header('Content-type', 'text/html')
        self.send_response(200)
        self.end_headers()

    def authenticate_payload(self, payload):
        if 'auth' in payload and 'token' in payload['auth']:
            return payload['auth']['token'] == self.server.auth_token
        else:
            return False

    def parse_payload(self, payload):
        self.server.log_file.log_event(time.asctime(), payload)

        # round_phase = self.get_round_phase(payload)

        # if round_phase != self.server.round_phase:
        #     self.server.round_phase = round_phase
        #     print('New round phase: %s' % round_phase)

    def get_round_phase(self, payload):
        if 'round' in payload and 'phase' in payload['round']:
            return payload['round']['phase']
        else:
            return None

    def get_kill(self, payload):
        if 'player' in payload and 'state' in payload['player'] and 'rounds_kills' in payload['player']['state']:
            return payload['player']['rounds_kills']
        else:
            return None

    def log_message(self, format, *args):
        """
        Prevents requests from printing into the console
        """
        return


# def handler(self, data: gamestate.GameState):
#     print(data.player.state.health)


async def start_server(handler):
    server = GSIServer(('localhost', 3001), 'caccamelone', RequestHandler, data_handler=handler)
    print(time.asctime(), '-', 'CS:GO GSI server starting')

    try:
        await server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        server.server_close()
        print(time.asctime(), '-', 'CS:GO GSI server stopped')

    # async with server:
    #




