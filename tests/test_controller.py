#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
from unittest.mock import Mock

# Third Party
import pytest
import requests_mock

# InOrbit
from sick_tag_loc_connector.api import Tag
from sick_tag_loc_connector.controller import SickTagLocMasterController
from sick_tag_loc_connector.models import (
    SickTagLocConfig,
    SickTagLocConfigModel,
    CONNECTOR_TYPE,
)


class TestSickTagLocMasterController:

    @pytest.fixture
    def m(self):
        with requests_mock.Mocker() as m:
            yield m

    @pytest.fixture
    def tags_data(self):
        return {
            "results": [
                {
                    "id": "12",
                    "alias": "pizza tracker",
                    "title": "0x2404638707AA",
                    "private": "0",
                    "description": "",
                    "feed": "1.0.0",
                    "updated": "2024-06-10 15:05:31.425717",
                    "created": "2023-12-18 21:37:53.746653",
                    "creator": "admin",
                    "version": "1.0.0",
                    "website": "https://pizza.com",
                    "type": "tag",
                    "tags": ["#yolo"],
                },
                {
                    "id": "12_test",
                    "alias": "pizza tracker test",
                    "title": "0x2404638707AA_test",
                    "private": "0_test",
                    "description": "test",
                    "feed": "1.0.0_test",
                    "updated": "2024-06-10 15:05:31.425717_test",
                    "created": "2023-12-18 21:37:53.746653_test",
                    "creator": "admin_test",
                    "version": "1.0.0_test",
                    "website": "https://pizza.com_test",
                    "type": "tag_test",
                    "tags": ["#yolo_test"],
                },
            ]
        }

    @pytest.fixture
    def sick_tag_loc_config(self, tags_data):
        model = SickTagLocConfigModel(
            sick_rtls_http_server_address="https://localhost/", sick_rtls_api_key="key"
        )
        return SickTagLocConfig(connector_type=CONNECTOR_TYPE, connector_config=model)

    def test_init(self, m, sick_tag_loc_config, tags_data):
        m.get(
            f"{sick_tag_loc_config.connector_config.get_rest_api_url()}/tags",
            json=tags_data,
        )
        controller = SickTagLocMasterController(sick_tag_loc_config)

        connector_config = sick_tag_loc_config.connector_config
        headers = {
            "X-ApiKey": sick_tag_loc_config.connector_config.sick_rtls_api_key,
            "Content-Type": "application/json",
        }
        url = connector_config.get_rest_api_url()

        assert controller.config is sick_tag_loc_config
        assert controller.rest_client.headers == headers
        assert controller.rest_client.url == url

        assert len(controller.connectors) == 2
        validations = 0
        for connector in controller.connectors:
            assert connector.config is sick_tag_loc_config
            assert isinstance(connector.tag, Tag)
            for data in tags_data["results"]:
                if data["id"] == connector.tag._id:
                    assert connector.tag.get_attrs_dict() == data
                    validations = validations + 1
        assert validations == len(controller.connectors)

    def test_start(self, m, sick_tag_loc_config, tags_data):
        m.get(
            f"{sick_tag_loc_config.connector_config.get_rest_api_url()}/tags",
            json=tags_data,
        )
        controller = SickTagLocMasterController(sick_tag_loc_config)

        for connector in controller.connectors:
            connector.start = Mock()

        controller.start()
        for connector in controller.connectors:
            connector.start.assert_called_once()

    def test_stop(self, m, sick_tag_loc_config, tags_data):
        m.get(
            f"{sick_tag_loc_config.connector_config.get_rest_api_url()}/tags",
            json=tags_data,
        )
        controller = SickTagLocMasterController(sick_tag_loc_config)

        for connector in controller.connectors:
            connector.stop = Mock()

        controller.stop()
        for connector in controller.connectors:
            connector.stop.assert_called_once()
