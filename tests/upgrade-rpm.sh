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

REPO_URL="${REPO_URL:-https://s3.amazonaws.com/hoot-repo}"
REPO_PREFIX="${REPO_PREFIX:-el7/develop}"

if [ -f el7/none.rpm ]; then
    echo "No new RPM to install and test with."
else
    # Install Hootenanny package.
    yum-config-manager --add-repo "${REPO_URL}/${REPO_PREFIX}/hoot.repo"
    yum makecache -y
    yum install -y hootenanny-services-ui

    # State the previous version.
    echo "previous hoot version: $(hoot version)"

    # Determine the version of the RPMs in the workspace.
    RPM_FILE="$(find el7 -type f -name hootenanny-autostart-\*noarch.rpm | head -n 1)"
    RPM_VERSION="$(echo "$RPM_FILE" | awk 'match($0, /hootenanny-autostart-(.+).noarch.rpm$/, a) { print a[1] }')"

    # Manually upgrade Hootenanny using the workspace RPMs.
    yum install -y \
        "el7/hootenanny-core-deps-$RPM_VERSION.noarch.rpm" \
        "el7/hootenanny-core-$RPM_VERSION.x86_64.rpm" \
        "el7/hootenanny-services-ui-$RPM_VERSION.x86_64.rpm"

    # State the upgraded version.
    echo "upgraded hoot version: $(hoot version)"
fi
