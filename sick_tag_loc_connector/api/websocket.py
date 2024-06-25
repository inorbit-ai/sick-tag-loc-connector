#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
import json
import logging
import threading
from typing import Callable, Union

# Third-party
import websocket

# InOrbit
from sick_tag_loc_connector.api import HEADER_API_KEY


class WebSocketClient:
    """WebSocketClient for SICK Streams

    A helper class that handles connections to a WebSocket server, listens for messages,
    and executes a callback function upon receiving messages.
    """

    def __init__(self, url: str, api_key: str, feed_id: str, on_message_cb: Callable):
        """WebSocketClient Constructor

        Initializes the WebSocketClient.

        Args:
            url (str): The WebSocket server URL to connect to
            api_key (str): The API Key to authenticate to the WebSocket
            feed_id (str): The SICK feed ID for this WebSocket client
            on_message_cb (Callable): Callback to execute when a message is received
        """
        self.logger = logging.getLogger(name=self.__class__.__name__)
        self.url = url
        self.headers = {HEADER_API_KEY: api_key}

        self.ws = None
        self.feed_id = feed_id
        self._on_message_cb = on_message_cb
        self._thread = None
        self.__connection_open = threading.Event()

    def on_error(self, error: str) -> None:
        """Error Callback

        Callback function to handle errors, by default this will simply log the error
        message.

        Args:
            error (str): The error message
        """
        self.logger.error(f"error: {error}")

    def on_close(self, code: int, msg: str) -> None:
        """Close Callback

        Callback function to handle the closing of the WebSocket connection.

        Args:
            code (int): Connection disconnect code
            msg (str): The disconnect message
        """
        self.logger.info(f"Connection closed for {self.url} -> {code}:'{msg}'")
        self.__connection_open.clear()

    def on_open(self) -> None:
        """Open Callback

        Callback function to handle the opening of the WebSocket connection.
        """
        self.logger.info(f"Connection opened for {self.url}")
        self.__connection_open.set()

    def on_message(self, msg: str) -> None:
        """
        Callback function to handle the messages from the WebSocket connection.

        Args:
            msg (str): Message received from the web socket connection.
        """
        if self._on_message_cb:
            self._on_message_cb(msg)
        else:
            self.logger.warning("on_message_cb function not configured")

    def send(self, data: Union[bytes, str]) -> None:
        """Main send function.

        Send a message through the WebSocket connection.

        Args:
            data (bytes | str): The data to send.
        """
        if self.ws and self.__connection_open.is_set():
            self.ws.send(data)
        else:
            self.logger.warning("WebSocket not connected - data not sent")

    def open(self) -> None:
        """Main connection method.

        Establish the WebSocket connection and start listening for messages.
        """
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=lambda ws, msg: self.on_message(msg),
            on_error=lambda ws, err: self.on_error(err),
            on_close=lambda ws, code, msg: self.on_close(code, msg),
            on_open=lambda ws: self.on_open(),
        )
        self._thread = threading.Thread(target=self.ws.run_forever)
        self._thread.start()
        # Wait until connection is open
        # TODO(russell): This needs a timeout
        self.__connection_open.wait()

    def close(self) -> None:
        """Main disconnection method.

        Close the WebSocket connection and stop the listening thread.
        """
        if self.ws:
            self.ws.close()
        if self._thread:
            self._thread.join()

    def connected(self) -> bool:
        """Connection Check

        Returns the status of the WebSocket connection.

        Returns:
            bool: If the connection is still open.
        """
        return self.__connection_open.is_set()

    def subscribe(self) -> None:
        """Subscribe to updates for the specific feed associated with this client.

        This method constructs a subscription message and sends it via the WebSocket
        connection.
        """
        if not self.connected():
            self.open()
        msg = (
            f'{{"headers":{json.dumps(self.headers).replace(": ", ":")}, '
            f'"method":"subscribe", "resource":"/feeds/{self.feed_id}"}}'
        )
        self.send(msg)
