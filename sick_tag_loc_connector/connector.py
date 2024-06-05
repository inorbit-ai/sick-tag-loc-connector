#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
import json

# InOrbit
from inorbit_connector.connector import Connector

from sick_tag_loc_connector.models import SickTagLocConfig
from sick_tag_loc_connector.api.websocket import WebSocketClient


class SickTagLocConnector(Connector):
    """InOrbit Connector for a SICK Tag.
    this represents a tag inside the SICK Tag Loc system

    TODO(elvio.aruta): Add a better description
    """

    def __init__(self, robot_id: str, config: SickTagLocConfig) -> None:
        """Initialize a new SICK Tag connector
        TODO(elvio.aruta): this represent a tag inside the SICK Tag Loc system

        Args:
            robot_id (str): The ID used in InOrbit of the Tag from the SICK Tag Loc system.
            config (SickTagLocConfig): The configuration for the connector.
        """

        self.config = config
        super().__init__(robot_id, self.config)
        self.poses_ws_client = None

    def connect(self) -> None:
        super()._connect()
        self._subscribe_to_pose_updates()

    def disconnect(self) -> None:
        super()._disconnect()
        self._unsubscribe_to_pose_updates()

    def start(self) -> None:
        super().start()

    def stop(self) -> None:
        super().stop()

    def execution_loop(self):
        super()._execution_loop()

    def _subscribe_to_pose_updates(self) -> None:
        # NOTE(elvio.aruta): self.config.ws_api_url is not defined
        # It should be defined inside SickTagLocConfig
        # Creates a new WebSocketClient
        self.poses_ws_client = WebSocketClient(self.config.ws_api_url)
        self.poses_ws_client.connect(self._publish_poses_on_inorbit)
        self.poses_ws_client.send(self._build_pose_subscription_messsage())

    def _get_feed_id(self) -> str:
        # TODO(elvio.aruta): get feed_id from Rest API
        feed_id = ""
        return feed_id

    def _build_pose_subscription_messsage(self) -> str:
        # TODO(elvio.aruta): get ws_api_key from SickTagLocConfig
        # config is still not defined
        ws_api_key = self.config.ws_api_key
        feed_id = self._get_feed_id()
        message = f'{{"headers":{{"X-ApiKey":"{ws_api_key}"}}, "method":"subscribe", "resource":"/feeds/{feed_id}"}}'
        return message

    def _unsubscribe_to_pose_updates(self) -> None:
        if self.poses_ws_client:
            self.poses_ws_client.close()
            self.poses_ws_client = None

    def _parse_pose_from_ws(self, msg_from_ws):
        parsed_json = json.loads(msg_from_ws)
        # Extract X, Y from the message
        datastreams = parsed_json["body"]["datastreams"]
        pose_data = {}
        for datastream in datastreams:
            if datastream["id"] == "posX":
                pose_data["x"] = datastream["current_value"].strip()
            elif datastream["id"] == "posY":
                pose_data["y"] = datastream["current_value"].strip()
        # NOTE(elvio.aruta): yaw? (probably not needed)
        return pose_data

    def _publish_poses_on_inorbit(self, msg) -> None:
        pose = self._parse_pose_from_ws(msg)
        # Add Edge SDK publish_pose() method from RobotSession
        # self.inorbit_sess.publish_pose(**pose)
        pass
