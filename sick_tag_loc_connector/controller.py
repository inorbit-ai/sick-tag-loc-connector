#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# InOrbit
from sick_tag_loc_connector.connector import SickTagLocConnector
from sick_tag_loc_connector.api.tag import Tag
from sick_tag_loc_connector.api.rest import RestClient
from sick_tag_loc_connector.models import SickTagLocConfig


class SickTagLocMasterController:
    """A controller class for managing SickTagLocConnectors.

    This class loads all tags from the system and creates and manages a set of
    SickTagLocConnectors based on configuration provided by SickTagLocConfig.
    """

    def __init__(self, config: SickTagLocConfig):
        """Initialize the SickTagLocMasterController

        A call to start/stop should be made after initialization.

        Args:
            config (SickTagLocConfig): Configuration object containing settings for
                                       connectors and API clients
        """
        self.config = config

        # Create (but don't start) the connection components
        self.rest_client = RestClient(
            self.config.connector_config.get_rest_api_url(),
            self.config.connector_config.sick_rtls_api_key,
        )
        tags = Tag.get_all(self.rest_client)
        self.connectors = [SickTagLocConnector(self.config, tag) for tag in tags]

    def start(self) -> None:
        """Start all SickTagLocConnectors managed by this controller.

        The connector list is initialized in the constructor of the class.
        """
        [connector.start() for connector in self.connectors]

    def stop(self) -> None:
        """Stop all SickTagLocConnectors managed by this controller.

        This method stops each active connector.
        """
        [connector.stop() for connector in self.connectors]

    # TODO(russell): add a "refresh" function to get and add new tags periodically
