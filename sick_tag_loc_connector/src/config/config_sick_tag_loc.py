#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
import os
from pathlib import Path
from typing import List

# Third-party
import pytz
from inorbit_edge.models import CameraConfig
from inorbit_edge.robot import INORBIT_CLOUD_SDK_ROBOT_CONFIG_URL
from pydantic import BaseModel, field_validator, HttpUrl

# InOrbit
from inorbit_connector.utils import LogLevels, DEFAULT_TIMEZONE, read_yaml
from inorbit_connector.models import InorbitConnectorConfig


class SickTagLocConfigModel(BaseModel):
    """A class representing the Instock abstract Model.

    SickTagLocConfigModel class is responsible for holding the configuration values related
    to the SICK Tag LOC API. It inherits from the BaseModel class.

    TODO(elvio.aruta98): add attributes
    Attributes:
        -
        -
        -
        -
    """

    pass


class SickTagLocConfig(InorbitConnectorConfig):
    connector_config: SickTagLocConfigModel
    pass


def load_and_validate(config_filename: str) -> SickTagLocConfig:
    """Loads and validates the configuration file.

    Raises an exception if the arguments or configuration are invalid.

    Args:
        config_filename (str): The YAML file to load the configuration from.
    Returns:
        SickTagLocConfig: The SICK Tag Loc configuration object with the loaded values.
    Raises:
        FileNotFoundError: If the configuration file does not exist.
        IndexError: If the configuration file does not contain the robot_id.
        yaml.YAMLError: If the configuration file is not valid YAML.
    """
    # NOTE(elvio.aruta98): this could change after some iterations
    # over this connector, don't take this like "the truth"
    # config = read_yaml(config_filename, robot_id)
    # Since this is maybe loaded from the master controller, I don't think we want to use
    # a robot id, probably a list of robotIds inside a configuration yaml
    return SickTagLocConfig()
