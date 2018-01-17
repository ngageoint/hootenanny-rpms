#!/bin/bash
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
