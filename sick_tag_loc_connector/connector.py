#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
import json
from typing import Union

# Third-party
from inorbit_connector.connector import Connector

from sick_tag_loc_connector.models import SickTagLocConfig
from sick_tag_loc_connector.api.websocket import WebSocketClient
from sick_tag_loc_connector.api.tag import Tag, TagStreamWebSocketClient

# Constants
RTLS_SICK_ID_PREFIX = "rtls-sick-"


class SickTagLocConnector(Connector):
    """
    InOrbit Connector for a SICK Tag.

    This class represents a tag inside the SICK Tag Loc system and handles the connection between
    the SICK Tag loc system and InOrbit
    """

    def __init__(self, tag: Tag, config: SickTagLocConfig) -> None:
        """
        Initialize a new SICK Tag connector.

        Args:
            tag (Tag): The Tag instance representing the SICK tag.
            config (SickTagLocConfig): Configuration object containing settings for the connector.
        """
        self.config = config
        self.tag = tag
        super().__init__(self._assign_inorbit_id(self.tag._id), self.config)
        self.connector_ws_client = None

    def connect(self) -> None:
        """
        Connect the SICK Tag connector and subscribe to pose updates.
        """
        super()._connect()
        self._subscribe_to_pose_updates()

    def disconnect(self) -> None:
        """
        Disconnect the SICK Tag connector and unsubscribe from pose updates.
        """
        super()._disconnect()
        self._unsubscribe_to_pose_updates()

    def execution_loop(self):
        super()._execution_loop()

    def _subscribe_to_pose_updates(self) -> None:
        """
        Subscribe to pose updates for the tag via WebSocket.

        This method initializes a new WebSocket client and subscribes to pose updates for the tag.
        """
        # Create a new TagStreamWebSocketClient with the necessary parameters
        self.connector_ws_client = TagStreamWebSocketClient(
            str(self.config.connector_config.sick_tag_loc_ws_url),
            self.config.connector_config.sick_tag_loc_ws_api_key,
            self.publish_poses_on_inorbit,
            self.tag,
        )

        self.connector_ws_client.connect()
        self.connector_ws_client.subscribe_to_tag_updates()

    def _unsubscribe_to_pose_updates(self) -> None:
        """
        Unsubscribe from pose updates for the tag.

        This method closes the WebSocket client and sets it to None.
        """
        if self.connector_ws_client:
            self.connector_ws_client.close()
            self.connector_ws_client = None

    def _parse_pose_from_ws(self, msg_from_ws: Union[bytes, str]) -> dict:
        """
        Parse the pose data from the WebSocket message.

        Args:
            msg_from_ws (Any): The message received from the WebSocket.

        Returns:
            dict: The parsed pose data containing 'x' and 'y' coordinates.
        """
        parsed_json = json.loads(msg_from_ws)
        datastreams = parsed_json["body"]["datastreams"]
        pose_data = {}
        for datastream in datastreams:
            if (ds_id := datastream["id"]) == "posX":
                pose_data["x"] = datastream["current_value"].strip()
            elif ds_id == "posY":
                pose_data["y"] = datastream["current_value"].strip()
        # NOTE (elvio.aruta): yaw? (probably not needed)
        return pose_data

    def publish_poses_on_inorbit(self, msg: Any) -> None:
        """
        Publish pose data on InOrbit.

        Args:
            msg (Any): The message received from the WebSocket.
        """
        pose = self._parse_pose_from_ws(msg)
        # Add Edge SDK publish_pose() method from RobotSession
        # self.inorbit_sess.publish_pose(**pose)
        pass

    def _assign_inorbit_id(self, tag_id: str) -> str:
        """
        Assign a unique InOrbit ID to the tag.

        Args:
            tag_id (str): The ID of the tag.

        Returns:
            str: The assigned InOrbit ID.
        """
        # NOTE (elvio.aruta): this is wrong and 100% must be changed
        # it doesn't ensure uniquess in the database
        return f"{RTLS_SICK_ID_PREFIX}{tag_id}"
