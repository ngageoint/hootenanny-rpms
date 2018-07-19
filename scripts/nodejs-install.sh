#!/bin/bash
# Copyright (C) 2018 Radiant Solutions (http://www.radiantsolutions.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
set -euo pipefail

# Ensure the release is stripped from version.
NODE_VERSION=$(echo $1 | awk -F- '{ print $1 }')

# Install the specific version of NodeJS and the yum version locking plugin.
yum install -q -y \
    nodejs-$NODE_VERSION nodejs-devel-$NODE_VERSION \
    yum-plugin-versionlock

# Version lock the NodeJS version to prevent inadvertent upgrades.
yum versionlock nodejs nodejs-devel
