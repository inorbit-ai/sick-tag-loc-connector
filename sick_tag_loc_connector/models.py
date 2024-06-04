#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# InOrbit
from inorbit_connector.models import InorbitConnectorConfig

# Third-party
from inorbit_connector.utils import read_yaml
from pydantic import BaseModel


class SickTagLocConfigModel(BaseModel):
    """A class representing the Instock abstract Model.

    SickTagLocConfigModel class is responsible for holding the configuration values
    related to the SICK Tag LOC API. It inherits from the BaseModel class.

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
    # TODO(elvio.aruta98): this could change after some iterations over this connector,
    #                      don't take this like "the truth"
    # Since this is maybe loaded from the controller, I don't think we want to use a
    # robot id, probably a list of robotIds inside a configuration yaml
    config = read_yaml(config_filename)
    return SickTagLocConfig(**config)
