#!/bin/bash

# Used by the makefile to build a hoot tar ball on vagrant

set -e
set -x

# For testing
export GIT_COMMIT=1042_new


if [ -z "$GIT_COMMIT" ]; then
    export GIT_COMMIT=develop
fi
echo $GIT_COMMIT

# NOTE: This is after we have removed the OpenJdk
export JAVA_HOME=/usr/java/jdk1.8.0_144

echo "%__make /usr/bin/make -sj4" >> /home/vagrant/.rpmmacros

cd /home/vagrant/hootenanny-rpms/src/

# This is needed by the Makefile
mkdir -p tmp

# Builds and installs necessary RPMs for archiving hoot
rm -f RPMS/x86_64/hoot*.rpm
make -j $((`nproc` + 2)) tmp/hoot-deps

# init and start Postgres
# Need to figure out a way to do this automagically
#PG_VERSION=9.5
PG_VERSION=$(psql --version | egrep -o '[0-9]{1,}\.[0-9]{1,}')

cd /tmp
sudo /usr/pgsql-$PG_VERSION/bin/postgresql95-setup initdb
sudo systemctl start postgresql-$PG_VERSION
sudo systemctl enable postgresql-$PG_VERSION

while ! PG_VERSION=$(sudo -u postgres psql -c 'SHOW SERVER_VERSION;' | egrep -o '[0-9]{1,}\.[0-9]{1,}'); do
    echo "Waiting for postgres to start"
    sleep 1
done


# create Hoot services db
if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw hoot; then
    sudo -u postgres createuser --superuser hoot || true
    sudo -u postgres psql -c "alter user hoot with password 'hoottest';"
    sudo -u postgres createdb hoot --owner=hoot
    sudo -u postgres createdb wfsstoredb --owner=hoot
    sudo -u postgres psql -d hoot -c 'create extension hstore;'
    sudo -u postgres psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='wfsstoredb'"
    sudo -u postgres psql -d wfsstoredb -c 'create extension postgis;'
    sudo -u postgres psql -d wfsstoredb -c "GRANT ALL on geometry_columns TO PUBLIC;"
    sudo -u postgres psql -d wfsstoredb -c "GRANT ALL on geography_columns TO PUBLIC;"
    sudo -u postgres psql -d wfsstoredb -c "GRANT ALL on spatial_ref_sys TO PUBLIC;"
fi
if ! sudo grep -i --quiet hoot /var/lib/pgsql/$PG_VERSION/data/pg_hba.conf; then
    sudo sed -i '1ihost    all            hoot            127.0.0.1/32            md5' /var/lib/pgsql/$PG_VERSION/data/pg_hba.conf
    sudo sed -i '1ihost    all            hoot            ::1/128                 md5' /var/lib/pgsql/$PG_VERSION/data/pg_hba.conf
    sudo systemctl restart postgresql-$PG_VERSION
fi

# Build the Hootenanny archive
cd /home/vagrant/hootenanny-rpms
mkdir -p tmp
cd tmp

rm -rf hootenanny
git clone https://github.com/ngageoint/hootenanny.git
cd hootenanny
git submodule update --init --recursive
git checkout $GIT_COMMIT
# Do a pull just in case a branch was specified.
git pull || echo "Ignore the failure."
git submodule update --init --recursive
cp LocalConfig.pri.orig LocalConfig.pri
echo "QMAKE_CXX=ccache g++" >> LocalConfig.pri

source SetupEnv.sh

# Configure makefiles, we aren't testing services with RPMs yet.
aclocal && autoconf && autoheader && automake --add-missing --copy && \
  ./configure --quiet --with-rnd --with-services --with-postgresql=/usr/pgsql-$PG_VERSION/bin/pg_config

if [ ! -f conf/database/DatabaseConfigDefault.sh ]; then
    cp conf/database/DatabaseConfig.sh.orig conf/database/DatabaseConfig.sh
fi

echo "### About to Make Clean ###"
make -s clean

# Remove any old archives
rm -f hootenanny-*.tar.gz hootenanny-services-*.war
rm -f /home/vagrant/hootenanny-rpms/src/SOURCES/hootenanny-*.tar.gz
rm -f /home/vagrant/hootenanny-rpms/src/SOURCES/hootenanny-services*.war

[ -e /tmp/words1.sqlite ] && cp /tmp/words1.sqlite conf/

echo "### About to Make Archive ###"
make -s -j `nproc` archive

cp -l hootenanny-[0-9]*.tar.gz /home/vagrant/hootenanny-rpms/src/SOURCES/
cp -l hootenanny-services*.war /home/vagrant/hootenanny-rpms/src/SOURCES/
