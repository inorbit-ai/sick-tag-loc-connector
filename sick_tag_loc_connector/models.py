#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
import os
from typing import Optional, List, Dict, Any
from urllib.parse import urlunparse

# Third Party
from inorbit_edge.robot import RobotFootprintSpec
from inorbit_connector.models import InorbitConnectorConfig
from inorbit_connector.utils import read_yaml
from pydantic import BaseModel, HttpUrl, field_validator, model_validator

# InOrbit
from sick_tag_loc_connector.api import REST_ENDPOINT

# Accepted/default values
CONNECTOR_TYPE = "sick_tag_loc"
DEFAULT_RTLS_REST_API_PORT = 8080
DEFAULT_RTLS_WS_PORT = 80


class SickTagLocConfigModel(BaseModel):
    """A class representing the SICK Tag-LOC attributes.

    SickTagLocConfigModel class is responsible for holding the configuration values
    related to the SICK Tag-LOC API. It inherits from the BaseModel class.

    Attributes:
        sick_rtls_http_server_address (HttpUrl): The URL of the SICK RTLS server
        sick_rtls_rest_api_port (int, optional): The port SICK RTLS REST API
        sick_rtls_websocket_port (int, optional): The port SICK RTLS WebSocket
        sick_rtls_api_key (str | None, optional): The SICK RTLS API key
        translation_x (float, optional): The coordinate translation in the X dimension
        translation_y (float, optional): The coordinate translation in the Y dimension
        footprints (Dict[str, RobotFootprintSpec], optional): List of defined
            footprints for tags. Should include the footprint and radius.
        tag_footprints (Dict[str, str]): Mapping of tag IDs to `RobotFootprintSpec`
            created after parsing the `footprint_specs` attribute.
    """

    sick_rtls_http_server_address: HttpUrl
    sick_rtls_rest_api_port: int = DEFAULT_RTLS_REST_API_PORT
    sick_rtls_websocket_port: int = DEFAULT_RTLS_WS_PORT
    sick_rtls_api_key: str = os.getenv("SICK_RTLS_API_KEY")
    translation_x: float = 0.0
    translation_y: float = 0.0
    footprints: Optional[List[Dict[str, Any]]] = {}
    tag_footprints: Dict[str, RobotFootprintSpec] = {}

    # noinspection PyMethodParameters
    @field_validator("sick_rtls_rest_api_port", "sick_rtls_websocket_port")
    def port_validation(cls, value: int) -> int:
        """Validates the SICK API ports.

        Validates the port is greater than 0 and less than 65536.

        Args:
            value (int): The SICK API port to validate

        Returns:
            str: The validated SICK API port

        Raises:
            ValueError: If the SICK API port
        """

        if value < 1 or value > 65535:
            raise ValueError("Invalid port")
        return value

    # noinspection PyMethodParameters
    @field_validator("sick_rtls_api_key")
    def check_whitespace(cls, value: str) -> str:
        """Check if the sick_rtls_api_key contains whitespace.

        This is used for the sick_rtls_api_key.

        Args:
            value (str): The sick_rtls_api_key to be checked

        Raises:
            ValueError: If the sick_rtls_api_key contains whitespace

        Returns:
            str: The given value if it does not contain whitespaces
        """

        if any(char.isspace() for char in value):
            raise ValueError("Whitespaces are not allowed")
        return value

    @model_validator(mode="before")
    def check_tag_footprints(cls, data):
        """Validate that the referenced footprint exists.

        Args:
            value (Dict[str, str]): The tag_footprints dictionary.

        Returns:
            Dict[str, str]: The given value if the referenced footprint exists.
        """
        footprints = data.get("footprints")

        if not footprints:
            return data

        data["tag_footprints"] = {}

        for custom_footprint in footprints:
            if not isinstance(custom_footprint, dict):
                raise ValueError("Footprint must be a dictionary")

            if not isinstance(custom_footprint.get("tags"), list):
                raise ValueError("Tags must be a list of tag IDs")

            if not isinstance(custom_footprint.get("spec"), dict):
                raise ValueError("Spec must be a dictionary")

            footprint = custom_footprint["spec"].get("footprint")
            radius = custom_footprint["spec"].get("radius")

            if not footprint and not radius:
                raise ValueError("At least one of footprint or radius must be provided")

            for tag_id in custom_footprint.get("tags"):
                if not isinstance(tag_id, str):
                    raise ValueError("Tag ID must be a string")

                data["tag_footprints"][tag_id] = RobotFootprintSpec(
                    footprint=footprint,
                    radius=radius,
                )

        return data

    def get_rest_api_url(self):
        """Returns the REST API URL for the Sick RTLS system.

        This will be built using the components in this model.

        Returns:
            The REST API URL as a string
        """
        scheme = self.sick_rtls_http_server_address.scheme
        netloc = (
            f"{self.sick_rtls_http_server_address.host}:{self.sick_rtls_rest_api_port}"
        )
        url = REST_ENDPOINT

        components = (scheme, netloc, url, "", "", "")
        return urlunparse(components)

    def get_websocket_url(self):
        """Returns the REST API URL for the Sick RTLS system.

        This will be built using the components in this model.

        Returns:
            The REST API URL as a string
        """
        scheme = "ws"
        netloc = (
            f"{self.sick_rtls_http_server_address.host}:{self.sick_rtls_websocket_port}"
        )

        components = (scheme, netloc, "", "", "", "")
        return urlunparse(components)


class SickTagLocConfig(InorbitConnectorConfig):
    """SICK Tag-LOC connector configuration schema.

    The main configuration for a SICK Tag-LOC connector instance.

    Attributes:
        connector_config (SickTagLocConfigModel): The configuration parameters
    """

    connector_config: SickTagLocConfigModel

    # noinspection PyMethodParameters
    @field_validator("connector_type")
    def check_connector_type(cls, connector_type: str) -> str:
        """Validate the connector type.

        This should always be equal to the pre-defined constant.

        Args:
            connector_type (str): The defined connector type passed in

        Returns:
            str: The validated connector type

        Raises:
            ValueError: If the connector type is not equal to the pre-defined constant
        """
        if connector_type != CONNECTOR_TYPE:
            raise ValueError(
                f"Expected connector type '{CONNECTOR_TYPE}' not '{connector_type}'"
            )
        return connector_type


def load_and_validate(config_filename: str) -> SickTagLocConfig:
    """Loads and validates the configuration file.

    Raises an exception if the arguments or configuration is invalid.

    Args:
        config_filename (str): The YAML file to load the configuration from

    Returns:
        SickTagLocConfig: The SICK Tag Loc configuration object with the loaded values

    Raises:
        FileNotFoundError: If the configuration file does not exist
        IndexError: If the configuration file does not contain the robot_id
        yaml.YAMLError: If the configuration file is not valid for YAML
    """
    config = read_yaml(config_filename)
    return SickTagLocConfig(**config)
