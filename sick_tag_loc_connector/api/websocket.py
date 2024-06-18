#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
import threading
import logging
from typing import Callable, Union

# Third-party
import websocket


class WebSocketClient:
    """WebSocketClient

    A helper class that handles connections to a WebSocket server, listens for messages,
    and executes a callback function upon receiving messages
    """

    def __init__(self, url: str, api_key: str, on_message_callback: Callable):
        """WebSocketClient Constructor

        Initializes the WebSocketClient.

        Args:
            url (str): The WebSocket server URL to connect to.
            api_key (str): The API Key to authenticate to the WebSocket.
            on_message_callback (Callable): Callback function to execute when a message
                                            is received
        """
        self.logger = logging.getLogger(name=self.__class__.__name__)
        self.url = url
        self.api_key = api_key
        self.on_message_callback = on_message_callback
        self.ws = None
        self.thread = None
        self.connection_open = threading.Event()

    def on_error(self, error: str) -> None:
        """
        Callback function to handle errors, by default this will simply log the error
        message.

        Args:
            error (str): The error message.
        """
        self.logger.error(f"error: {error}")

    def on_close(self, code: int, msg: str) -> None:
        """
        Callback function to handle the closing of the WebSocket connection.

        Args:
            code (int): Connection disconnect code
            msg (str): The disconnect message
        """
        self.logger.info(f"Connection closed for {self.url} -> {code}:'{msg}'")
        self.connection_open.clear()

    def on_open(self) -> None:
        """
        Callback function to handle the opening of the WebSocket connection.
        """
        self.logger.info(f"Connection opened for {self.url}")
        self.connection_open.set()

    def on_message(self, msg: str) -> None:
        """
        Callback function to handle the messages from the WebSocket connection.

        Args:
            msg (str): Message received from the web socket connection.
        """
        if self.on_message_callback:
            self.on_message_callback(msg)
        else:
            self.logger.warning("on_message_callback function not configured")

    def send(self, data: Union[bytes, str]) -> None:
        """
        Send a message through the WebSocket connection.

        Args:
            data (bytes | str): The data to send.
        """
        if self.ws and self.connection_open.is_set():
            self.ws.send(data)
        else:
            self.logger.warning(
                "WebSocketApp not initialized, or connection not open, data will not be sent."
            )

    def connect(self) -> None:
        """
        Establish the WebSocket connection and start listening for messages.
        """
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=lambda ws, msg: self.on_message(msg),
            on_error=lambda ws, err: self.on_error(err),
            on_close=lambda ws, code, msg: self.on_close(code, msg),
            on_open=lambda ws: self.on_open(),
        )
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.start()
        # Wait until connection is open
        self.connection_open.wait()

    def close(self) -> None:
        """
        Close the WebSocket connection and stop the listening thread.
        """
        if self.ws:
            self.ws.close()
        if self.thread:
            self.thread.join()
