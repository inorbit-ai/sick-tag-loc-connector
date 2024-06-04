#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

from sick_tag_loc_connector.connector import SickTagLocConnector


# TODO(elvio.aruta98): This class needs some logic to read the config and be able to
#                      create the needed connectors!
#                      Also, it should interact with the rest API to get info from there
#                      (existent tags? tag last state? filter existent tags with the
#                       ones defined in the config?)


class SickTagLocMasterController:
    def __init__(self):
        self.connectors = []

    def create_connector(self, tag_id, connector_config):
        connector = SickTagLocConnector(tag_id, connector_config)
        self.connectors.append(connector)
        return connector

    def start_all(self):
        for connector in self.connectors:
            connector.start()

    def stop_all(self):
        for connector in self.connectors:
            connector.stop()
