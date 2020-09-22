import requests
import jwt
from urllib.parse import urlencode
import websocket, json, time


try:
    import thread
except ImportError:
    import _thread as thread

class upbitCalssWs():
    def __init__(self):
        self.access_key = 'cMrjCW3yR5a1GssxO4qzTskOpteHj37T0Nd2jwlY'
        self.secret_key = 'd86eqJpNqXCTxex5zqMtkiPZ5mW6oM5jQU5cqbhk'
        self.ws = websocket.WebSocketApp("ws://api.upbit.com/websocket/v1",
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        self.ws.on_open = self.on_open

    def on_message(self, message):
        json_data = json.loads(message)
        print(json_data)

    def on_error(self, error):
        print(error)

    def on_close(self):
        print('### closed ###')

    def on_open(self):
        def run(*args):
            self.ws.send(json.dumps(
                [{"ticket": "test"}, {"type": "ticker", "codes": ["KRW-BTC"]}]
            ))
        thread.start_new_thread(run,())


    websocket.enableTrace(True)




#ws.run_forever()



