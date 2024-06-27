#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
from unittest.mock import MagicMock
import logging
import threading

# Third-party
import pytest
from websocket import WebSocketApp

# InOrbit
from sick_tag_loc_connector.api.websocket import WebSocketClient


class TestWebSocketClient:
    @pytest.fixture
    def ws_client(self):
        return WebSocketClient(
            "ws://test-url",
            "key",
            "my_feed_id",
            MagicMock(),
        )

    @pytest.fixture
    def mock_websocket(self):
        return MagicMock(spec=WebSocketApp)

    def test_init(self, ws_client):
        assert ws_client.url == "ws://test-url"
        assert ws_client.headers == {"X-ApiKey": "key"}
        assert ws_client.feed_id == "my_feed_id"
        assert isinstance(ws_client._on_message_cb, MagicMock)
        assert isinstance(ws_client.logger, logging.Logger)
        assert ws_client.ws is None
        assert ws_client._thread is None
        assert ws_client.connected() is False

    def test_on_message(self, ws_client):
        on_message_cb = MagicMock()
        ws_client._on_message_cb = on_message_cb
        ws_client.on_message("test_message")
        on_message_cb.assert_called_once_with("test_message")

    def test_send_no_websocket(self, ws_client, mock_websocket):
        ws_client.ws = None
        ws_client.send("test_data")
        mock_websocket.send.assert_not_called()
        assert ws_client.connected() is False

    def test_send_not_connected(self, ws_client, mock_websocket):
        ws_client.ws = mock_websocket
        ws_client.send("test_data")
        mock_websocket.send.assert_not_called()
        assert ws_client.connected() is False

    def test_send(self, ws_client):
        ws_client.on_open()
        ws_client.open()
        ws_client.ws.send = MagicMock()
        assert ws_client.connected() is True
        ws_client.send("test_data")
        ws_client.ws.send.assert_called_once_with("test_data")

    def test_open(self, ws_client):
        ws_client.on_open()
        ws_client.open()
        assert ws_client.connected() is True
        assert ws_client.url == ws_client.ws.url

    def test_close(self, ws_client, mock_websocket):
        ws_client.ws = mock_websocket
        ws_client._thread = MagicMock(spec=threading.Thread)
        ws_client.close()
        mock_websocket.close.assert_called_once()
        ws_client._thread.join.assert_called_once()

    def test_on_message_cb_execution(self, ws_client):
        on_message_cb = MagicMock()
        ws_client._on_message_cb = on_message_cb
        ws_client.on_message("test_message")
        on_message_cb.assert_called_once_with("test_message")

    def test_subscribe(self, ws_client):
        ws_client.on_open()
        ws_client.open()
        ws_client.ws.send = MagicMock()
        assert ws_client.connected() is True
        ws_client.subscribe()
        ws_client.ws.send.assert_called_once_with(
            '{"headers":{"X-ApiKey":"key"},'
            '"method":"subscribe",'
            '"resource":"/feeds/my_feed_id"}'
        )

    def test_subscribe_no_open(self, ws_client, mock_websocket):
        assert ws_client.connected() is False
        ws_client.on_open()
        ws_client.ws = mock_websocket
        ws_client.subscribe()
        ws_client.ws.send.assert_called_once_with(
            '{"headers":{"X-ApiKey":"key"},'
            '"method":"subscribe",'
            '"resource":"/feeds/my_feed_id"}'
        )
        assert ws_client.connected() is True
