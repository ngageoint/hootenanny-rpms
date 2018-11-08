#!/usr/bin/dumb-init /bin/bash
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

# Create logfiles.
touch /var/log/{node-export,node-mapnik,tomcat8}.log
chown tomcat:tomcat /var/log/{node-export,node-mapnik,tomcat8}.log

# PostgreSQL
su-exec postgres pg_ctl -D $PGDATA -s start &> /dev/null

# Tomcat
su-exec tomcat /usr/libexec/tomcat8/server start &> /var/log/tomcat8.log &

su-exec tomcat bash -c "cd /var/lib/hootenanny/node-export-server && npm start" &> /var/log/node-export.log &

# Start command as the Tomcat user.
exec su-exec tomcat $@
