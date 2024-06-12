import pytest
from unittest.mock import MagicMock
from websocket import WebSocketApp
import logging
import threading
from sick_tag_loc_connector.api.websocket import WebSocketClient


class TestWebSocketClient:
    @pytest.fixture
    def ws_client(self):
        return WebSocketClient("ws://test-url", "key", MagicMock())

    @pytest.fixture
    def mock_websocket(self):
        return MagicMock(spec=WebSocketApp)

    def test_init(self, ws_client):
        assert ws_client.url == "ws://test-url"
        assert ws_client.api_key == "key"
        assert isinstance(ws_client.on_message_callback, MagicMock)
        assert isinstance(ws_client.logger, logging.Logger)
        assert ws_client.ws is None
        assert ws_client.thread is None

    def test_on_message(self, ws_client):
        on_message_callback = MagicMock()
        ws_client.on_message_callback = on_message_callback
        ws_client.on_message("test_message")
        on_message_callback.assert_called_once_with("test_message")

    def test_send(self, ws_client, mock_websocket):
        ws_client.ws = mock_websocket
        ws_client.send("test_data")
        mock_websocket.send.assert_called_once_with("test_data")

    def test_connect(self, ws_client, mock_websocket):
        ws_client.ws = mock_websocket
        mock_call_back = MagicMock()
        ws_client.on_message_callback = mock_call_back
        ws_client.connect()
        assert ws_client.url == ws_client.ws.url

    def test_close(self, ws_client, mock_websocket):
        ws_client.ws = mock_websocket
        ws_client.thread = MagicMock(spec=threading.Thread)
        ws_client.close()
        mock_websocket.close.assert_called_once()
        ws_client.thread.join.assert_called_once()

    def test_on_message_callback_execution(self, ws_client):
        test_message = "test_message"
        on_message_callback = ws_client.on_message_callback
        ws_client.on_message(test_message)
        on_message_callback.assert_called_once_with(test_message)
