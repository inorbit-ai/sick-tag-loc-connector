#!/bin/bash

# Get script directory
SCRIPT_PATH=`readlink -f $0`
SCRIPT_DIR=`dirname $SCRIPT_PATH`
# Change to the connector directory
cd $SCRIPT_DIR/..

ENV_FILE=config/.env
VENV_DIR=.venv

if [ -z "$1" ]; then
    echo "Usage: $0 <config_basename> [<args>]"
    echo "Example: \`$0 local -v\` runs the Connector with the 'config/local.yaml' configuration and the flag '-v'"
    echo ""
    echo "  The script will start the InOrbit SICK Tag-LOC RTLS Connector with the specified YAML configuration from the config directory. Extra arguments will be passed to the Connector."
    echo "  The Connector will be run in a virtual environment located in the '`realpath $VENV_DIR`' directory."
    echo "  If '`realpath $ENV_FILE`' exists, its variables will be exported. It is a good place to set environment variables like \`INORBIT_API_KEY\`."
    echo "  Available configurations:"
    ls config/*.yaml | xargs -n 1 basename | sed 's/\.yaml//'
    exit 1
fi

# Parameters
FILE_BASENAME=`echo $1 | rev | cut -d. -f2- | rev`  # Get all but last column (allowing for file basenames with dots)
CONFIG_FILE=config/$FILE_BASENAME.yaml
CONNECTOR_ARGS=${@:2}

if [ ! -f $CONFIG_FILE ]; then
    echo "Configuration file $CONFIG_FILE not found"
    exit 1
fi
if [ ! -f $VENV_DIR/bin/activate ]; then
    echo "Virtual environment not found."
    exit 1
fi

if [ ! -f $ENV_FILE ]; then
    echo "Warning: Environment file $ENV_FILE not found"
else
    echo "Exporting variables from $ENV_FILE"
    # Get all environment variables from the .env file and export them
    export $(grep -v '^#' $ENV_FILE | xargs)
fi

# Activate the virtual environment
source $VENV_DIR/bin/activate
# Start the connector
sick-tag-loc-connector -c $CONFIG_FILE $CONNECTOR_ARGS
