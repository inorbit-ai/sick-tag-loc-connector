#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

from typing import List

from sick_tag_loc_connector.connector import SickTagLocConnector
from sick_tag_loc_connector.api.tag import Tag
from sick_tag_loc_connector.api.rest import RestClient
from sick_tag_loc_connector.models import SickTagLocConfig

class SickTagLocMasterController:

    def __init__(self, config: SickTagLocConfig):
        self.connectors = []
        self.config = config
        self.rest_client = RestClient(
            self.config.connector_config.sick_tag_loc_rest_api_url,
            self.config.connector_config.sick_tag_loc_rest_api_key,
        )

    def start_controller(self):
        self._create_connectors()
        for connector in self.connectors:
            connector.start()

    def stop_controller(self):
        for connector in self.connectors:
            connector.stop()

    def _create_connectors(self):
        tags = self._get_all_tags()
        self.connectors = [SickTagLocConnector(tag, self.config) for tag in tags]

    def _get_all_tags(self) -> List[Tag]:
        return Tag.get_all(self.rest_client)
