#!/bin/bash

set -e

OKGREEN='\033[92m'
# WARNING='\033[93m'
FAIL='\033[91m'
OKBLUE='\033[94m'
UNDERLINE='\033[4m'
ENDC='\033[0m'

echo "Installing dependancies  ..."
cat dependencies.txt | xargs -a brew install -y
echo -e "${OKGREEN} ✓ ${ENDC} complete"

echo "Preparing usbboot submodule  ..."
git submodule update --init --recursive
cd usboot
make
echo -e "${OKGREEN} ✓ ${ENDC} complete"