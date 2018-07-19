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

PG_DOTLESS=$(echo $PG_VERSION | tr -d '.')

# Install PostgreSQL server and contrib package (for hstore).
yum -q -y install \
    postgresql$PG_DOTLESS-contrib \
    postgresql$PG_DOTLESS-server

# Install alternatives for `initdb` and `pg_ctl` so we won't have to
# muck with $PATH.
alternatives --install /usr/bin/initdb pgsql-initdb \
             /usr/pgsql-$PG_VERSION/bin/initdb 500
alternatives --install /usr/bin/pg_ctl pgsql-pg_ctl \
             /usr/pgsql-$PG_VERSION/bin/pg_ctl 500

# Initialize the database as `postgres` user.
su-exec postgres initdb -D $PGDATA --locale $LANG
