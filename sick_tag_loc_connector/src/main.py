#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (C) 2024 InOrbit, Inc.

import argparse
import logging
from time import sleep

from sick_tag_loc_connector.src.config.config_sick_tag_loc import load_and_validate
from sick_tag_loc_connector.src.controller import SickTagLocMasterController


# TODO(russell): abstract to higher level library
def main():
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
        f"Running with the following:\n" f"\tabstract: {config_file}\n" f"\tverbose: {verbose}"
    )

    try:
        # Parse the YAML
        sic_tag_loc_config = load_and_validate(config_file)
    except FileNotFoundError:
        logger.error(f"'{config_file}' configuration file does not exist")
        exit(1)

    # Start master controller here
    # Master controller should start all the needed connectors
    # using the sic_tag_loc_config
    # master_controller = MasterController(sic_tag_loc_config)
    # Example usage:
    controller = SickTagLocMasterController()

    # Create connectors
    # NOTE(elvio.aruta98): here we need a "create all connectors" method
    # leaving a draft here to catch the idea, but they shouldn't be created individually
    # there should be some logic to create them all using the config
    controller.create_connector(sic_tag_loc_config)
    controller.create_connector(sic_tag_loc_config)
    controller.create_connector(sic_tag_loc_config)

    # Start all connectors
    controller.start_all()

    try:
        while True:
            # Yield execution to another thread
            sleep(0)
    except KeyboardInterrupt:
        logger.info("...exiting")
        controller.stop_all()


if __name__ == "__main__":
    main()
