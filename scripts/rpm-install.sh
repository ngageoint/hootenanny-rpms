#!/bin/bash
set -euo pipefail

# Installs RPM tools on Debian and RHEL-like platforms.
LSB_DIST="$(. /etc/os-release && echo "$ID")"
if [ "$LSB_DIST" == 'centos' -o "$LSB_DIST" == 'fedora' -o "$LSB_DIST" == 'rhel' ]; then
    sudo yum install -q -y rpm-build
elif [ "$LSB_DIST" == 'debian' -o "$LSB_DIST" == 'ubuntu' ]; then
    sudo apt-get update -qq
    sudo apt-get install -qq -y rpm
fi
