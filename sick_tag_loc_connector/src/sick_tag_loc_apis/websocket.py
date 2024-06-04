# TODO(elvio.aruta98): Add to requirements and pick the right version
import websocket


class WebSocketClient:
    def __init__(self, uri, subscription_message):
        self.uri = uri
        self.subscription_message = subscription_message
        self.message_callback = message_callback

    async def connect(self):
        uri = "ws://localhost:8001"  # Change the URI to match your server address
        ws = websocket.WebSocketApp(uri, on_message=on_message)

    async def subscribe(self, websocket):
        await websocket.send(self.subscription_message)
        print(f"Sent: {self.subscription_message}")

    async def receive_messages(self, websocket):
        while True:
            message = await websocket.recv()
            self.message_callback(message)

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.connect())


def message_handler(message):
    print(f"Received message: {message}")
    # Add your custom logic here to handle the message


# Replace 'wss://example.com/websocket' with your WebSocket server URL
uri = "wss://example.com/websocket"
# Customize the subscription message
subscription_message = '{"type": "subscribe", "channel": "example_channel"}'

client = WebSocketClient(uri, subscription_message, message_handler)
client.run()
