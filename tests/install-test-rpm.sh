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
set -euxo pipefail

if [ -f el7/none.rpm ]; then
    echo "No new RPM to install and test with."
else
    # Determine the version of the RPMs in the workspace.
    RPM_FILE="$(find el7 -type f -name hootenanny-autostart-\*noarch.rpm | head -n 1)"
    RPM_VERSION="$(echo "$RPM_FILE" | awk 'match($0, /hootenanny-autostart-(.+).noarch.rpm$/, a) { print a[1] }')"

    # Manually install Hootenanny from the workspace RPMs.
    yum install -y "el7/hootenanny-core-deps-$RPM_VERSION.noarch.rpm"
    yum install -y "el7/hootenanny-core-$RPM_VERSION.x86_64.rpm"
    yum install -y "el7/hootenanny-services-ui-$RPM_VERSION.x86_64.rpm"

    # Setup database for testing.
    ./scripts/postgresql-install.sh
    ./scripts/hoot-db-setup.sh
    su-exec postgres pg_ctl -D "$PGDATA" -s start

    # Start Tomcat and node-export and send output to logfiles.
    touch /var/log/{node-export,tomcat8}.log
    chown tomcat:tomcat /var/log/{node-export,tomcat8}.log
    su-exec tomcat /usr/libexec/tomcat8/server start &> /var/log/tomcat8.log &
    su-exec tomcat bash -c "cd /var/lib/hootenanny/node-export-server && npm start" &> /var/log/node-export.log &

    # Run Hootenanny tests.
    cd /var/lib/hootenanny
    su-exec tomcat HootTest --diff --quick --parallel "$(nproc)"
fi
