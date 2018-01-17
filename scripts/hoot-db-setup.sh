#!/bin/bash
set -euo pipefail

POSTGRES_CONF=$PGDATA/postgresql.conf
POSTGRES_HBA=$PGDATA/pg_hba.conf

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
listen_addresses = '127.0.0.1'
shared_buffers = 1024MB
max_files_per_process = 1000
work_mem = 16MB
maintenance_work_mem = 256MB
#checkpoint_segments = 20
autovacuum = off
EOF

# Very permissive pg_hba.conf to ease in initial setup.
cat > $POSTGRES_HBA <<EOF
local   all             all                                     trust
EOF

# Start database.
su-exec postgres pg_ctl -D $PGDATA -w start

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
su-exec postgres pg_ctl -D $PGDATA -w stop

# Lockdown pg_hba.conf to requiring passwords.
cat > $POSTGRES_HBA <<EOF
host    all             all             127.0.0.1/32            md5
EOF
