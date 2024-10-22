#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
import json
from typing import Union

# Third-party
from inorbit_connector.connector import Connector

# InOrbit
from sick_tag_loc_connector.models import SickTagLocConfig
from sick_tag_loc_connector.api.tag import Tag


class SickTagLocConnector(Connector):
    """InOrbit Connector for a SICK Tag.

    This class represents a tag inside the SICK Tag-LOC system and handles the
    communication between the SICK Tag loc system and InOrbit.

    Attributes:
        config (SickTagLocConfig): The configuration for this connector
        tag (Tag): The SICK tag associated with this connector
        websocket_client (TagStreamWebSocketClient | None): The Tag WebSocket connection
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

        This method also calls the super method to connect to InOrbit, and applies the
        footprint settings if provided.
        """
        # Connect to InOrbit
        super()._connect()

        self.websocket_client = self.tag.get_websocket_client(
            self.config.connector_config.sick_rtls_websocket_port,
            self._parse_pose_from_ws,
        )
        self.websocket_client.subscribe()

        # If a footprint spec was provided, apply it
        tag_id = self.tag.get_inorbit_id()
        if footprint := self.config.connector_config.tag_footprints.get(tag_id):
            self._logger.debug(f"Applying footprint {footprint} to tag {tag_id}")
            self._robot_session.apply_footprint(footprint)

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

    def _parse_pose_from_ws(self, msg_from_ws: Union[bytes, str]) -> None:
        """Parse the pose data from the WebSocket message.

        If a valid pose message is found, self._last_pose is set.

        Args:
            msg_from_ws (bytes | str): The message received from the WebSocket.
        """
        parsed_json = json.loads(msg_from_ws)
        datastreams = parsed_json["body"]["datastreams"]
        pose_data = {}
        for datastream in datastreams:
            if (ds_id := datastream["id"]) == "posX":
                pose_data["x"] = float(datastream["current_value"].strip())
            elif ds_id == "posY":
                pose_data["y"] = float(datastream["current_value"].strip())
        if "x" in pose_data and "y" in pose_data:
            pose_data["yaw"] = float("inf")
            self._last_pose = self._transform(pose_data)

    def _transform(self, pose: dict) -> dict:
        """Main transform between the SICK pose into an InOrbit pose.

        This method will read values from the config. Note that no rotation applied
        since the SICK system doesn't provide theta and is assumed to be aligned with
        zero radians.

        Args:
            pose (dict): A dict with x,y values

        Returns:
            A fully transformed pose
        """
        # Translation
        x = pose["x"] - self.config.connector_config.translation_x
        # Note that the "y" coordinates are reversed in the SICK system
        y = -pose["y"] - self.config.connector_config.translation_y

        return {"x": x, "y": y, "yaw": pose["yaw"]}
