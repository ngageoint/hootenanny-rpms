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

REPO_BUCKET="${REPO_BUCKET:-hoot-repo}"
REPO_PREFIX="${REPO_PREFIX:-el7/develop}"
SLACK_NOTIFY="${SLACK_NOTIFY:-yes}"
SLACK_USER="${SLACK_USER:-circleci_bot}"

if [ -f el7/none.rpm ]; then
    echo "RPM has already been created."
else
    # Get the version of the RPM in the workspace.
    RPM_FILE="$(find el7 -type f -name hootenanny-autostart-\*noarch.rpm | head -n 1)"
    RPM_VERSION="$(echo "$RPM_FILE" | awk 'match($0, /hootenanny-autostart-(.+).noarch.rpm$/, a) { print a[1] }')"

    # Synchronize the new RPMs from the workspace with those in the
    # repository bucket/prefix.
    ./scripts/repo-sync.sh -d el7 -b "$REPO_BUCKET" -p "$REPO_PREFIX" -q

    # Send slack notification when repository has been updated.
    if [ "$SLACK_NOTIFY" = "yes" ]; then
        ./scripts/slack-notify.sh \
            -c "$SLACK_CHANNEL" \
            -t "$SLACK_TOKEN" \
            -u "$SLACK_USER" \
            -m "Hootenanny Develop Repository Updated to \`$RPM_VERSION\`"
    fi
fi
