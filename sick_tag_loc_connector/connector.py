#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Third-party
from inorbit_connector.connector import Connector

# InOrbit
from sick_tag_loc_connector.api.websocket import WebSocketClient
from sick_tag_loc_connector.models import SickTagLocConfig


class SickTagLocConnector(Connector):
    """InOrbit Connector for a SICK Tag.

    TODO(elvio.aruta98): Add a better description
                         this represents a tag inside the SICK Tag Loc system
    """

    def __init__(self, tag_id: str, config: SickTagLocConfig) -> None:
        """Initialize a New SICK Tag Connector

        TODO(elvio.aruta98): Add a better description
                             this represent a tag inside the SICK Tag Loc system

        Args:
            tag_id (str): Tag ID from the SICK system for use in InOrbit
            config (SickTagLocConfig): The configuration for the connector
        """

        self.config = config
        super().__init__(tag_id, self.config)

    def connect(self) -> None:
        super()._connect()
        self._subscribe_to_pose_updates()

    def disconnect(self) -> None:
        super()._disconnect()
        self.unsubscribe()

    def start(self) -> None:
        super().start()

    def stop(self) -> None:
        super().stop()

    def execution_loop(self):
        super()._execution_loop()

    def _subscribe_to_pose_updates(self):
        # It should subscribe to UDP/WEBSOCKET in SICK Tag Loc
        # It could be taken from the config, depending on the use case
        # (lower ms response from UDP) Also it could try to subscribe first to one,
        # and if it fails after "x" retries it could try with another protocol
        # (websocket connection failed 10 times? -> subscribes to UDP)
        self._logger.info("subscribed to updates!")
        # TODO(elvio.aruta98): get url from config here
        ws_client = WebSocketClient("wss://web-socket-url-from-sick-tag-loc")
        ws_client.connect(self._publish_poses)

    def unsubscribe(self):
        self._logger.info("unsubscribed from updates!")

    def _publish_poses(self):
        pass
