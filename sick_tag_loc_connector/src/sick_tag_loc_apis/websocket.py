# Example of a websocket client oriented to callback execution when messages are received
# Not tested, left here for easy development in the future

import websocket
import threading
import json


class WebSocketClient:

    def __init__(self, url):
        self.url = url
        self.ws = None
        self.callback = None
        self.running = False

    def on_message(self, ws, message):
        if self.callback:
            self.callback(message)

    def on_error(self, ws, error):
        print(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print(f"Closed: {close_status_code} - {close_msg}")
        self.running = False

    def on_open(self, ws):
        print("Connection opened")

    def connect(self, callback):
        self.callback = callback
        self.ws = websocket.WebSocketApp(
            self.url, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close
        )
        self.ws.on_open = self.on_open
        self.running = True

        # Run the WebSocket in a separate thread to avoid blocking
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.start()

    def send(self, message):
        if self.ws and self.ws.sock and self.ws.sock.connected:
            self.ws.send(message)
        else:
            print("WebSocket is not connected.")

    def close(self):
        self.running = False
        if self.ws:
            self.ws.close()
        if self.thread:
            self.thread.join()
