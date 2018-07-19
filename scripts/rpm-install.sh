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

# Installs RPM tools on Debian and RHEL-like platforms.
LSB_DIST="$(. /etc/os-release && echo "$ID")"
if [ "$LSB_DIST" == 'centos' -o "$LSB_DIST" == 'fedora' -o "$LSB_DIST" == 'rhel' ]; then
    sudo yum install -q -y rpm-build
elif [ "$LSB_DIST" == 'debian' -o "$LSB_DIST" == 'ubuntu' ]; then
    sudo apt-get update -qq
    sudo apt-get install -qq -y rpm
fi
