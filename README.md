# sick-tag-loc-connector
A Python connector for the SICK Tag-LOC RTLS into InOrbit.

## Overview

<!-- TODO -->

## Features

<!-- TODO -->

## Requirements

<!-- TODO -->

## Setup

<!-- TODO: Install from PyPi instructions

There are two ways for installing the connector Python package.

1. From PyPi: `pip install inorbit-instock-connector`

2. From source: clone the repository and install the dependencies: -->

From source: clone the repository and install the dependencies:

```bash
virtualenv .venv
. .venv/bin/activate
pip install -e .
```

Configure the Connector:

- Copy [`config/example.yaml`](config/example.yaml) and modify the settings to match your setup.

- Copy [`config/example.env`](config/example.env) to `config/.env` and set the environment variables following the instructions in the same
  file. You can get the `INORBIT_API_KEY` for your account from InOrbit's
  [Developer Console](https://developer.inorbit.ai/docs#configuring-environment-variables).

## Deployment

### Run the Connector manually

Once all dependencies are installed and the configuration is complete, the Connector can be run with the  `sick-tag-loc-connector` command (run with `--help` for details).

```bash
# Add the environment variables, activate the virtual environment and run the Connector
export $(grep -v '^#' config/.env | xargs) && \
source .venv/bin/activate && \
sick-tag-loc-connector -c config/example.yaml
```

A [script](scripts/start.sh) was provided to help run the Connector.

```
❯ ./scripts/start.sh 
Usage: ./scripts/start.sh <config_basename> [<args>]
Example: `./scripts/start.sh local -v` runs the Connector with the 'config/local.yaml' configuration and the flag '-v'

  The script will start the InOrbit SICK Tag-LOC RTLS Connector with the specified YAML configuration from the config directory. Extra arguments will be passed to the Connector.
  The Connector will be run in a virtual environment located in the '/home/tomas/InOrbit/sick-tag-loc-connector/.venv' directory.
  If '/home/tomas/InOrbit/sick-tag-loc-connector/config/.env' exists, its variables will be exported. It is a good place to set environment variables like `INORBIT_API_KEY`.
  Available configurations:
example
```

### Run the Connector as a service

<!-- TODO -->

## Next Steps

<!-- TODO -->
