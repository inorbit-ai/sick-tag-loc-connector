#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
import json
from typing import Union, Any

# Third-party
from inorbit_connector.connector import Connector

from sick_tag_loc_connector.models import SickTagLocConfig
from sick_tag_loc_connector.api.tag import Tag, TagStreamWebSocketClient


class SickTagLocConnector(Connector):
    """InOrbit Connector for a SICK Tag.

    This class represents a tag inside the SICK Tag-LOC system and handles the
    communication between the SICK Tag loc system and InOrbit.

    Attributes:
        config (SickTagLocConfig): The configuration for this connector
        tag (Tag): The SICK tag associated with this connector
        websocket_client (TagStreamWebSocketClient | None): The Tag Websocket connection
    """

    def __init__(self, config: SickTagLocConfig, tag: Tag) -> None:
        """
        Initialize a new SICK Tag connector.

        Args:
            tag (Tag): The SICK tag associated with this connector
            config (SickTagLocConfig): The configuration for this connector
        """
        super().__init__(tag.get_inorbit_id(), config)

        self.config = config
        self.tag = tag
        self.websocket_client = None
        self._last_pose = None
        self._last_pose_sent = None

    def _connect(self) -> None:
        """Connect the SICK Tag connector and subscribe to updates.

        This method also calls the super method to connect to InOrbit.
        """
        super()._connect()

        # TODO(russell): Change to self.tag.create_websocket_client()
        self.websocket_client = TagStreamWebSocketClient(
            self.config.connector_config.get_websocket_url(),
            self.config.connector_config.sick_rtls_api_key,
            self._publish_poses_on_inorbit,
            self.tag,
        )

        self.websocket_client.connect()
        # TODO(russell/elvio): Might be better to just have this called in connect
        self.websocket_client.subscribe_to_tag_updates()

    def _disconnect(self) -> None:
        """Disconnect the SICK Tag connector and unsubscribe from updates.

        This method also calls the super method to disconnect to InOrbit.
        """
        super()._disconnect()

        if self.websocket_client:
            self.websocket_client.close()
            self.websocket_client = None
            self._last_pose = None
            self._last_pose_sent = None

    def _execution_loop(self):
        """Send updated poses.

        This will only publish on a change in position.
        """
        if self._last_pose != self._last_pose_sent:
            self._robot_session.publish_pose(**self._last_pose)
            self._last_pose_sent = self._last_pose

    @staticmethod
    def _parse_pose_from_ws(msg_from_ws: Union[bytes, str]) -> dict:
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
                pose_data["x"] = float(datastream["current_value"].strip())
            elif ds_id == "posY":
                pose_data["y"] = float(datastream["current_value"].strip())
        pose_data["yaw"] = float("-inf")
        return pose_data

    def _publish_poses_on_inorbit(self, msg: Any) -> None:
        """
        Publish pose data on InOrbit.

        Args:
            msg (Any): The message received from the WebSocket.
        """
        pose = self._parse_pose_from_ws(msg)
        pose = self._apply_poses_transformation(pose)
        self._last_pose = pose

    @staticmethod
    def _apply_poses_transformation(pose) -> dict:
        # TODO(elvio.aruta): complete this method
        # Method to transform (x,y) poses from RTLS system
        # to the correct (x,y) poses displayed in InOrbit
        # TODO: (elvio.aruta): Create a data structure for pose
        return pose
