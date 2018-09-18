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

POSTGRES_CONF=$PGDATA/postgresql.conf
POSTGRES_HBA=$PGDATA/pg_hba.conf
TOMCAT_SERVER=/usr/libexec/tomcat8/server
TOMCAT_WEBAPPS=/var/lib/tomcat8/webapps

DB_NAME="${DB_NAME:-hoot}"
DB_NAME_OSMAPI="${DB_NAME_OSMAPI:-osmapi_test}"
DB_USER="${DB_USER:-hoot}"
DB_PASSWORD="${DB_PASSWORD:-hoottest}"
WFS_DB_NAME="${WFS_DB_NAME:-wfsstoredb}"

sed -i s/^max_connections/\#max_connections/ $POSTGRES_CONF
sed -i s/^shared_buffers/\#shared_buffers/ $POSTGRES_CONF

cat >> $POSTGRES_CONF <<EOF

#--------------
# Hoot Settings
#--------------
max_connections = 1000
shared_buffers = 1024MB
max_files_per_process = 1000
work_mem = 16MB
maintenance_work_mem = 256MB
autovacuum = off
EOF

# Very permissive pg_hba.conf to ease in initial setup.
if ! grep -i --quiet hoot $POSTGRES_HBA; then
    sed -i '1ihost    all            hoot            127.0.0.1/32            md5' $POSTGRES_HBA
    sed -i '1ihost    all            hoot            ::1/128                 md5' $POSTGRES_HBA
fi

# Start database.
su-exec postgres pg_ctl -D $PGDATA -s -w start

# Create hoot database user.
createuser --username postgres --superuser $DB_USER
psql --username postgres --dbname postgres --command \
     "ALTER USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';"

# Create hoot database, with hstore.
createdb --username postgres $DB_NAME --owner $DB_USER
psql --username postgres --dbname $DB_NAME --command \
     "CREATE EXTENSION hstore;"

# Create hoot WFS database template, with PostGIS.
createdb --username postgres $WFS_DB_NAME --owner $DB_USER
psql --username postgres --dbname $WFS_DB_NAME --command \
     "CREATE EXTENSION postgis; GRANT ALL ON geography_columns, geometry_columns, spatial_ref_sys TO PUBLIC;"
psql --username postgres --dbname postgres --command \
     "UPDATE pg_database SET datistemplate='true' WHERE datname='${WFS_DB_NAME}';"

# Stop database.
su-exec postgres pg_ctl -D $PGDATA -s -m fast -w stop

# Setup that only occurs for runtime containers.
if rpm -qa | grep -q ^hootenanny ; then
    su-exec postgres pg_ctl -D $PGDATA -s -w start
    source $HOOT_HOME/conf/database/DatabaseConfig.sh

    # Run `SetupOsmApiDB.sh`, and clean up its logfile.
    $HOOT_HOME/scripts/database/SetupOsmApiDB.sh
    rm -f /tmp/osmapidb.log

    # Modify the Tomcat server context to include the processed ingest files.
    sed -i "s@<\/Host>@      <Context docBase=\""${HOOT_HOME//\//\\\/}"\/userfiles\/ingest\/processed\" path=\"\/static\" \/>\n      &@" \
        /etc/tomcat8/server.xml

    # Start Tomcat, and wait for it to unpack the hoot-services WAR,
    # as it's where we'll update liquibase.
    su-exec tomcat $TOMCAT_SERVER start &> /dev/null &
    echo -n 'Waiting for tomcat to start.'
    while ! test -d $TOMCAT_WEBAPPS/hoot-services/WEB-INF; do
        sleep 1
        echo -n '.'
    done
    echo ' done.'

    # Update liquibase.
    pushd $TOMCAT_WEBAPPS/hoot-services/WEB-INF
    JDBC_JAR="$(ls lib/postgresql-*.jar)"
    liquibase --contexts=default,production \
        --changeLogFile=classes/db/db.changelog-master.xml \
        --promptForNonLocalDatabase=false \
        --driver=org.postgresql.Driver \
        --url=jdbc:postgresql://$DB_HOST:$DB_PORT/$DB_NAME \
        --username=$DB_USER \
        --password=$DB_PASSWORD \
        --logLevel=warning \
        --classpath=$JDBC_JAR \
        update

    popd

    su-exec tomcat $TOMCAT_SERVER stop &> /dev/null &
    su-exec postgres pg_ctl -D $PGDATA -s -m fast -w stop
fi
