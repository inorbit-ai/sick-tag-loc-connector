#!/bin/bash

# Installs a systemd service for the sick-tag-loc-connector

# Get script directory
SCRIPT_PATH=`readlink -f $0`
SCRIPT_DIR=`dirname $SCRIPT_PATH`
# Change to the connector directory
cd $SCRIPT_DIR/..

if [ $# -eq 0 ]; then
    echo "Usage: $0 [--uninstall] <config_basename>"
    echo "This script will create and enable /etc/systemd/system/sick-tag-loc-connector@<config_basename>.service"
    echo "The service will run the InOrbit SICK Tag-LOC Connector with the <config_basename>.yaml configuration"
    echo "If --uninstall is passed it will stop and remove the service"
    echo ""
    echo "  Available configurations:"
    ls config/*.yaml | xargs -n 1 basename | sed 's/\.yaml//'
    exit 1
fi

echo This script will run commands with sudo. You may be prompted for your password
read -n 1 -r -p "Do you wish to continue? [Y/n]" ans;
case "$ans" in
    n|N)
        exit 1;;
    Y|y|"")
        ;;
    *)
        exit 1;;
esac
echo ""

START_SCRIPT_LOCATION=`realpath scripts/start.sh`
DESTINATION_START_SCRIPT="/usr/local/bin/sick-tag-loc-connector.sh"

# Uninstall procedure
if [ "$1" == "--uninstall" ]; then
    if [ $# -ne 2 ]; then
        echo "Usage: $0 --uninstall <service_name>"
        echo Missing service name
        exit 1
    fi
    SYSTEMD_SERVICE_NAME="sick-tag-loc-connector@$2.service"

    echo Uninstalling systemd service $SYSTEMD_SERVICE_NAME
    sudo systemctl stop $SYSTEMD_SERVICE_NAME
    sudo systemctl disable $SYSTEMD_SERVICE_NAME
    sudo rm /etc/systemd/system/$SYSTEMD_SERVICE_NAME
    sudo systemctl daemon-reload

    echo Removing $DESTINATION_START_SCRIPT
    sudo rm $DESTINATION_START_SCRIPT
    exit 0
fi

NAME=$1
TEMPLATE=`realpath scripts/sick-tag-loc-connector@.service`
SYSTEMD_SERVICE_NAME="sick-tag-loc-connector@$1.service"

echo Note: The user in the \`User=\` field in $TEMPLATE defines the user that will run the Connector.
echo "If such user doesn't exist it can be created with \`useradd <username>\`"
echo If you wish to run the service as a different user, edit the \`User=\` field in $TEMPLATE before continuing.
read -n 1 -s -r -p "Press any key to continue"
echo ""
echo ""

echo "Creating systemd service $SYSTEMD_SERVICE_NAME"
sudo systemctl stop $SYSTEMD_SERVICE_NAME
sudo cp $TEMPLATE /etc/systemd/system/$SYSTEMD_SERVICE_NAME
sudo systemctl daemon-reload

echo Installing symlink to $START_SCRIPT_LOCATION in $DESTINATION_START_SCRIPT
sudo ln -sf $START_SCRIPT_LOCATION $DESTINATION_START_SCRIPT

echo ""
echo To start the service run:
echo "	sudo systemctl start $SYSTEMD_SERVICE_NAME"
echo To stop the service run:
echo "	sudo systemctl stop $SYSTEMD_SERVICE_NAME"
echo To enable the service at boot run:
echo "	sudo systemctl enable $SYSTEMD_SERVICE_NAME"
echo Watch logs with:
echo "	sudo journalctl -u $SYSTEMD_SERVICE_NAME -f"
