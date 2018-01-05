#!/bin/bash
set -e

NODE_VERSION=$1

# Install the specific version of NodeJS and the yum version locking plugin.
yum install -q -y \
    nodejs-$NODE_VERSION nodejs-devel-$NODE_VERSION \
    yum-plugin-versionlock

# Version lock the NodeJS version to prevent inadvertent upgrades.
yum versionlock nodejs*
