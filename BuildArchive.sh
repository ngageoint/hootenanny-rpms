#!/bin/bash

# Used by the makefile to build a hoot tar ball on vagrant

####################################
#
# NOTE: This script assumes that all of the dependencies are installed!
# This means that the BuildDeps script has been run
#
####################################

set -e
set -x

if [ -z "$GIT_COMMIT" ]; then
    export GIT_COMMIT=develop
fi
echo "Building Hootenanny: $GIT_COMMIT"


cd /home/vagrant/hootenanny-rpms/

# This is needed by the Makefile
mkdir -p tmp
cd tmp

# Build the Hootenanny archive
rm -rf hootenanny
git clone https://github.com/ngageoint/hootenanny.git
cd hootenanny
git submodule update --init --recursive
git checkout $GIT_COMMIT
# Do a pull just in case a branch was specified.
git pull || echo "Ignore the failure."
git submodule update --init --recursive

cp LocalConfig.pri.orig LocalConfig.pri

source SetupEnv.sh

# Setup the Hootenanny database
if [ ! -f conf/database/DatabaseConfigDefault.sh ]; then
    cp conf/database/DatabaseConfig.sh.orig conf/database/DatabaseConfig.sh
fi

source $HOOT_HOME/conf/database/DatabaseConfig.sh

# Need to go somewhere that the postgres user can read/write to avoid warnings.
pushd /tmp

PG_VERSION=$(psql --version | egrep -o '[0-9]{1,}\.[0-9]{1,}')
# See if we already have a dB user
if ! sudo -u postgres psql -c "\du" | grep -iw --quiet $DB_USER; then
    echo "### Adding a Services Database user..."
    sudo -u postgres createuser --superuser $DB_USER
    sudo -u postgres psql -c "alter user $DB_USER with password '$DB_PASSWORD';"
fi

# Check that the OsmApiDb user exists
# NOTE:
#  + The OsmAPI Db user _might_ be different to the Hoot Services Db user...
#  + The SetupOsmApiDB.sh script expects that the DB_USER_OSMAPI account exists
if ! sudo -u postgres psql -c "\du" | grep -iw --quiet $DB_USER_OSMAPI; then
    sudo -u postgres createuser --superuser $DB_USER_OSMAPI
    sudo -u postgres psql -c "alter user $DB_USER_OSMAPI with password '$DB_PASSWORD_OSMAPI';"
fi

# Check for a hoot Db
if ! sudo -u postgres psql -lqt | grep -iw --quiet $DB_NAME; then
    echo "### Creating Services Database..."
    sudo -u postgres createdb $DB_NAME --owner=$DB_USER
    sudo -u postgres createdb wfsstoredb --owner=$DB_USER
    sudo -u postgres psql -d $DB_NAME -c 'create extension hstore;'
    sudo -u postgres psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='wfsstoredb'" > /dev/null
    sudo -u postgres psql -d wfsstoredb -c 'create extension postgis;' > /dev/null
fi

# configure Postgres settings
PG_HB_CONF=/var/lib/pgsql/$PG_VERSION/data/pg_hba.conf
if ! sudo -u postgres grep -i --quiet hoot $PG_HB_CONF; then
    sudo -u postgres cp $PG_HB_CONF $PG_HB_CONF.orig
    sudo -u postgres sed -i '1ihost    all            hoot            127.0.0.1/32            md5' $PG_HB_CONF
    sudo -u postgres sed -i '1ihost    all            hoot            ::1/128                 md5' $PG_HB_CONF
fi
POSTGRES_CONF=/var/lib/pgsql/$PG_VERSION/data/postgresql.conf
if ! sudo -u postgres grep -i --quiet HOOT $POSTGRES_CONF; then
    sudo -u postgres cp $POSTGRES_CONF $POSTGRES_CONF.orig
    sudo -u postgres sed -i s/^max_connections/\#max_connections/ $POSTGRES_CONF
    sudo -u postgres sed -i s/^shared_buffers/\#shared_buffers/ $POSTGRES_CONF
    sudo -u postgres bash -c "cat >> $POSTGRES_CONF" <<EOT
#--------------
# Hoot Settings
#--------------
max_connections = 1000
shared_buffers = 1024MB
max_files_per_process = 1000
work_mem = 16MB
maintenance_work_mem = 256MB
#checkpoint_segments = 20
autovacuum = off
EOT
fi

echo "Restarting postgres"
sudo systemctl restart postgresql-$PG_VERSION

# Back to Hootenanny
popd

# Configure Hoot
aclocal && autoconf && autoheader && automake --add-missing --copy && \
  ./configure --quiet --with-rnd --with-services --with-postgresql=/usr/pgsql-$PG_VERSION/bin/pg_config

echo "### Make Clean ###"
make -sj$(nproc) clean

# Remove any old archives
rm -f hootenanny-*.tar.gz hootenanny-services-*.war
rm -f /home/vagrant/hootenanny-rpms/SOURCES/hootenanny-*.tar.gz
rm -f /home/vagrant/hootenanny-rpms/SOURCES/hootenanny-services*.war

# This hopes that we have already installed the hootenanny-words RPM so we don't have to
# download it again.
[ -e /var/lib/hootenanny/conf/words1.sqlite ] && cp /var/lib/hootenanny/conf/words1.sqlite conf/

echo "### Make Archive ###"
make -s -j$(nproc) archive
echo "### Make Archive: Done ###"

cp -l hootenanny-[0-9]*.tar.gz /home/vagrant/hootenanny-rpms/SOURCES/
cp -l hootenanny-services*.war /home/vagrant/hootenanny-rpms/SOURCES/
