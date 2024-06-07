#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
from typing import List

# InOrbit
from sick_tag_loc_connector.connector import SickTagLocConnector
from sick_tag_loc_connector.api.tag import Tag
from sick_tag_loc_connector.api.rest import RestClient
from sick_tag_loc_connector.models import SickTagLocConfig

class SickTagLocMasterController:
    """
    A controller class for managing SickTagLocConnectors.

    This class handles the initialization and control of multiple SickTagLocConnectors based
    on configuration provided by SickTagLocConfig.
    """

    def __init__(self, config: SickTagLocConfig):
        """
        Initialize the SickTagLocMasterController.

        Args:
            config (SickTagLocConfig): Configuration object containing settings for connectors
                                       and REST client.
        """
        self.connectors = []
        self.config = config
        self.rest_client = RestClient(
            self.config.connector_config.sick_tag_loc_rest_api_url,
            self.config.connector_config.sick_tag_loc_rest_api_key,
        )

    def start_controller(self) -> None:
        """
        Start all SickTagLocConnectors managed by this controller.

        This method creates connectors based on available tags and starts each connector.
        """
        self._create_connectors()
        for connector in self.connectors:
            connector.start()

    def stop_controller(self) -> None:
        """
        Stop all SickTagLocConnectors managed by this controller.

        This method stops each active connector.
        """
        for connector in self.connectors:
            connector.stop()

    def _create_connectors(self) -> None:
        """
        Create SickTagLocConnectors for each tag obtained from the REST client.

        This method fetches all tags and initializes a SickTagLocConnector for each tag.
        """
        tags = self._get_all_tags()
        self.connectors = [SickTagLocConnector(tag, self.config) for tag in tags]

    def _get_all_tags(self) -> List[Tag]:
        """
        Fetch all tags from the REST API.

        Returns:
            List[Tag]: A list of Tag instances obtained from the REST API.
        """
        return Tag.get_all(self.rest_client)
