#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (C) 2024 InOrbit, Inc.

# Standard
# import html
# import json
# import threading

# Third Party
from inorbit_edge.commands import COMMAND_MESSAGE
from inorbit_edge.robot import COMMAND_CUSTOM_COMMAND
from requests import HTTPError

from inorbit_connector.connector import Connector
from sick_tag_loc_connector.src.config import SickTagLocConfig
from sick_tag_loc_apis.websocket import WebSocketClient


class SickTagConnector(Connector):
    """InOrbit Connector for a SICK Tag.
    this represents a tag inside the SICK Tag Loc system

    TODO(elvio.aruta98): Add a better description
    """

    def __init__(self, robot_id: str, config: SickTagLocConfig) -> None:
        """Initialize a new SICK Tag connector
        TODO(elvio.aruta98): this represent a tag inside the SICK Tag Loc system

        Args:
            robot_id (str): The ID used in InOrbit of the Tag from the SICK Tag Loc system.
            config (SickTagLocConfig): The configuration for the connector.
        """

        self.config = config
        super().__init__(robot_id, self.config)

    def connect(self) -> None:
        super()._connect()
        self.subscribe_to_websocket()

    def disconnect(self) -> None:
        super()._disconnect()
        self.unsubscribe()

    def start(self) -> None:
        super().start()

    def stop(self) -> None:
        super().stop()

    def execution_loop(self):
        super()._execution_loop()

    def subscribe_to_websocket(self):
        # It should suscribe to UDP/WEBSOCKET in SICK Tag Loc
        # It could be taken from the config, depending on the use case (lower ms response from UDP)
        # also it could try to suscribe first to one, and if it fails after "x" retries it could try
        # with another protocol (websocket connection failed 10 times? -> suscribes to UDP)
        self._logger.info("subscribed to updates!")
        # NOTE(elvio.aruta98): get url from config here
        ws_client = WebSocketClient(
            "wss://web-socket-url-from-sick-tag-loc"
        )  # Replace with your WebSocket URL
        ws_client.connect(self._publish_poses)

    def unsubscribe(self):
        self._logger.info("unsubscribed from updates!")

    def _publish_poses(self):
        pass
