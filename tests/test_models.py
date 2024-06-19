#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
import importlib
import os
import sys
from unittest.mock import Mock, patch

# Third Party
import pytest

# InOrbit
import sick_tag_loc_connector.models
from sick_tag_loc_connector.api import RestClient
from sick_tag_loc_connector.models import (
    load_and_validate,
    DEFAULT_RTLS_REST_API_PORT,
    DEFAULT_RTLS_WS_PORT,
    CONNECTOR_TYPE,
)


class TestSickTagLocConfigModel:

    def test_correct_config_model(self):
        model = sick_tag_loc_connector.models.SickTagLocConfigModel(
            sick_rtls_http_server_address="https://localhost/",
            sick_rtls_rest_api_port=8000,
            sick_rtls_websocket_port=8001,
            sick_rtls_api_key="key",
        )
        assert str(model.sick_rtls_http_server_address) == "https://localhost/"
        assert model.sick_rtls_rest_api_port == 8000
        assert model.sick_rtls_websocket_port == 8001
        assert model.sick_rtls_api_key == "key"

    def test_correct_config_model_defaults(self):
        model = sick_tag_loc_connector.models.SickTagLocConfigModel(
            sick_rtls_http_server_address="https://localhost/",
        )
        assert str(model.sick_rtls_http_server_address) == "https://localhost/"
        assert model.sick_rtls_rest_api_port == DEFAULT_RTLS_REST_API_PORT
        assert model.sick_rtls_websocket_port == DEFAULT_RTLS_WS_PORT
        assert model.sick_rtls_api_key is None

    @patch.dict(os.environ, {"SICK_RTLS_API_KEY": "keep-it-secret"})
    def test_correct_config_model_env_key(self):
        # Re-import after Mock
        importlib.reload(sys.modules["sick_tag_loc_connector.models"])
        model = sick_tag_loc_connector.models.SickTagLocConfigModel(
            sick_rtls_http_server_address="https://localhost/",
            sick_rtls_rest_api_port=8000,
            sick_rtls_websocket_port=8001,
        )
        assert str(model.sick_rtls_http_server_address) == "https://localhost/"
        assert model.sick_rtls_rest_api_port == 8000
        assert model.sick_rtls_websocket_port == 8001
        assert model.sick_rtls_api_key == "keep-it-secret"

    def test_ws_rest_validation(self):
        with pytest.raises(ValueError, match="Invalid port"):
            sick_tag_loc_connector.models.SickTagLocConfigModel(
                sick_rtls_http_server_address="https://localhost/",
                sick_rtls_rest_api_port=0,
                sick_rtls_api_key="key",
            )

        with pytest.raises(ValueError, match="Invalid port"):
            sick_tag_loc_connector.models.SickTagLocConfigModel(
                sick_rtls_http_server_address="https://localhost/",
                sick_rtls_rest_api_port=65536,
                sick_rtls_api_key="key",
            )

    def test_ws_port_validation(self):
        with pytest.raises(ValueError, match="Invalid port"):
            sick_tag_loc_connector.models.SickTagLocConfigModel(
                sick_rtls_http_server_address="https://localhost/",
                sick_rtls_websocket_port=0,
                sick_rtls_api_key="key",
            )

        with pytest.raises(ValueError, match="Invalid port"):
            sick_tag_loc_connector.models.SickTagLocConfigModel(
                sick_rtls_http_server_address="https://localhost/",
                sick_rtls_websocket_port=65536,
                sick_rtls_api_key="key",
            )

    def test_api_key_whitespace_check(self):
        with pytest.raises(ValueError, match="Whitespaces are not allowed"):
            sick_tag_loc_connector.models.SickTagLocConfigModel(
                sick_rtls_http_server_address="https://localhost/",
                sick_rtls_rest_api_port=8000,
                sick_rtls_websocket_port=8001,
                sick_rtls_api_key="bad key",
            )

    def test_get_rest_api_url(self):
        model = sick_tag_loc_connector.models.SickTagLocConfigModel(
            sick_rtls_http_server_address="https://localhost/",
            sick_rtls_rest_api_port=8000,
        )
        url = model.get_rest_api_url()
        assert url == "https://localhost:8000/sensmapserver/api"

    def test_get_websocket_url(self):
        model = sick_tag_loc_connector.models.SickTagLocConfigModel(
            sick_rtls_http_server_address="https://localhost/",
            sick_rtls_websocket_port=9000,
        )
        assert model.get_websocket_url() == "ws://localhost:9000"

    def test_tag_footprints_validation(self):
        model = sick_tag_loc_connector.models.SickTagLocConfigModel(
            sick_rtls_http_server_address="https://localhost/",
            footprints=[
                {
                    "tags": ["tagId1", "tagId7"],
                    "spec": {
                        "footprint": [
                            {"x": -0.5, "y": -0.5},
                            {"x": 0.3, "y": -0.5},
                            {"x": 0.3, "y": 0.5},
                            {"x": -0.5, "y": 0.5},
                        ],
                        "radius": 1,
                    },
                },
                {"tags": ["tagId3"], "spec": {"radius": 0.2}},
            ],
        )
        assert model.tag_footprints["tagId1"].footprint == [
            {"x": -0.5, "y": -0.5},
            {"x": 0.3, "y": -0.5},
            {"x": 0.3, "y": 0.5},
            {"x": -0.5, "y": 0.5},
        ]
        assert model.tag_footprints["tagId1"].radius == 1
        assert model.tag_footprints["tagId3"].radius == 0.2

        with pytest.raises(
            ValueError, match="At least one of footprint or radius must be provided"
        ):
            sick_tag_loc_connector.models.SickTagLocConfigModel(
                sick_rtls_http_server_address="https://localhost/",
                footprints=[
                    {
                        "tags": ["tagId1", "tagId7"],
                        "spec": {},
                    },
                ],
            )
        with pytest.raises(
            ValueError, match="At least one of footprint or radius must be provided"
        ):
            sick_tag_loc_connector.models.SickTagLocConfigModel(
                sick_rtls_http_server_address="https://localhost/",
                footprints=[
                    {
                        "tags": ["tagId1", "tagId7"],
                        "spec": {},
                    },
                ],
            )
        with pytest.raises(ValueError, match="Spec must be a dictionary"):
            sick_tag_loc_connector.models.SickTagLocConfigModel(
                sick_rtls_http_server_address="https://localhost/",
                footprints=[
                    {
                        "tags": ["tagId1", "tagId7"],
                        "spec": "invalid",
                    },
                ],
            )
        with pytest.raises(ValueError, match="Tags must be a list"):
            sick_tag_loc_connector.models.SickTagLocConfigModel(
                sick_rtls_http_server_address="https://localhost/",
                footprints=[
                    {
                        "tags": "invalid",
                        "spec": {
                            "footprint": [
                                {"x": -0.5, "y": -0.5},
                                {"x": 0.3, "y": -0.5},
                                {"x": 0.3, "y": 0.5},
                                {"x": -0.5, "y": 0.5},
                            ],
                            "radius": 1,
                        },
                    },
                ],
            )


class TestSickTagLocConfig:

    @pytest.fixture
    def mock_rest_client(self):
        return Mock(spec=RestClient)

    @pytest.fixture
    def sick_tag_loc_config_model(self):
        return sick_tag_loc_connector.models.SickTagLocConfigModel(
            sick_rtls_http_server_address="https://localhost/", sick_rtls_api_key="key"
        )

    def test_connector_config(self, sick_tag_loc_config_model):
        config = sick_tag_loc_connector.models.SickTagLocConfig(
            connector_type=CONNECTOR_TYPE,
            connector_config=sick_tag_loc_config_model,
        )
        assert config.connector_config is sick_tag_loc_config_model
        assert config.connector_type == CONNECTOR_TYPE

    def test_invalid_connector_type(self, sick_tag_loc_config_model):
        with pytest.raises(
            ValueError, match=f"Expected connector type '{CONNECTOR_TYPE}' not 'no'"
        ):
            sick_tag_loc_connector.models.SickTagLocConfig(
                connector_type="no", connector_config=sick_tag_loc_config_model
            )


class TestLoadAndValidate:

    @pytest.fixture
    def mock_rest_client(self):
        return Mock(spec=RestClient)

    def test_nonexistent_file(self):
        with pytest.raises(
            FileNotFoundError, match="No such file or directory: 'no.yaml"
        ):
            load_and_validate("no.yaml")

    def test_valid_yaml_file(self):
        file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../config/example.yaml"
        )
        config = load_and_validate(file)

        assert config.location_tz == "America/Los_Angeles"
        assert config.log_level == "INFO"
        assert config.connector_type == CONNECTOR_TYPE
        assert config.update_freq == 5.0

        address = str(config.connector_config.sick_rtls_http_server_address)
        assert address == "http://192.168.1.249/"
        assert config.connector_config.sick_rtls_rest_api_port == 8080
        assert config.connector_config.sick_rtls_websocket_port == 8080
