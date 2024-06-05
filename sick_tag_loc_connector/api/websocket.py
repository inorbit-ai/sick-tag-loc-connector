#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
import threading
import logging

# Third Party
import websocket

class WebSocketClient:
    """WebSocketClient

    A helper class that handles connections to a WebSocket server, listens for messages,
    and executes a callback function upon receiving messages
    """
    def __init__(self, url, on_message_callback):
        """WebSocketClient Constructor

        Initializes the WebSocketClient.

        Args:
            url: The WebSocket server URL to connect to.
            on_message_callback: Callback function to execute when a message is received
        """
        self.logger = logging.getLogger(name=self.__class__.__name__)
        self.url = url
        self.on_message_callback = on_message_callback
        self.ws = None
        self.thread = None

    def on_error(self, error) -> None:
        """
        Callback function to handle errors.

        Args:
            error: The error message.
        """
        self.logger.error(f"error: {error}")

    def on_close(self) -> None:
        """
        Callback function to handle the closing of the WebSocket connection.
        """
        self.logger.info(f"Connection closed for {self.url}")

    def on_open(self) -> None:
        """
        Callback function to handle the opening of the WebSocket connection.
        """
        self.logger.info(f"Connection opened for {self.url}")

    def on_message(self, msg) -> None:
        if self.on_message_callback:
            self.on_message_callback(msg)
        else:
            self.logger.warning(f"warning: on message callback function not configured")

    def send(self, data) -> None:
        """
        Send a message through the WebSocket connection.

        Args:
            data: The data to send.
        """
        if self.ws:
            self.ws.send(data)

    def connect(self) -> None:
        """
        Establish the WebSocket connection and start listening for messages.

        Args:
        on_message_callback: The callback function to handle incoming messages.
        """
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=lambda ws, msg: self.on_message(msg),
            on_error=lambda ws, err: self.on_error(err),
            on_close=lambda ws: self.on_close(),
            on_open=lambda ws: self.on_open(),
        )
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.start()

    def close(self) -> None:
        """
        Close the WebSocket connection and stop the listening thread.
        """
        if self.ws:
            self.ws.close()
        if self.thread:
            self.thread.join()
