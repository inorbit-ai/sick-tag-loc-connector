#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
import argparse
import logging
from time import sleep

# InOrbit
from sick_tag_loc_connector.controller import SickTagLocMasterController
from sick_tag_loc_connector.models import load_and_validate


def start():
    """The SICK Tag-LOC Connector

    This method is the entry point for starting the application.
    """
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--config",
        type=str,
        required=True,
        help="Path to the YAML file containing the robot configuration",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Output verbose information (main entry point only)",
    )

    # Read arguments
    args = parser.parse_args()
    config_file, verbose = args.config, args.verbose

    # Set logging
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logger.debug(
        f"Running with the following:\n"
        f"\tabstract: {config_file}\n"
        f"\tverbose: {verbose}"
    )

    try:
        # Parse the YAML
        sic_tag_loc_config = load_and_validate(config_file)
    except FileNotFoundError:
        logger.error(f"'{config_file}' configuration file does not exist")
        exit(1)

    controller = SickTagLocMasterController(sic_tag_loc_config)
    controller.start()

    try:
        while True:
            # Yield execution to another thread
            sleep(0)
    except KeyboardInterrupt:
        logger.info("...exiting")
        controller.stop()


if __name__ == "__main__":
    start()
