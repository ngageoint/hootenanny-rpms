#!/bin/bash

# Used by the makefile to build a hoot tar ball on vagrant

set -e
set -x

if [ -z "$GIT_COMMIT" ]; then
    export GIT_COMMIT=develop
fi
echo $GIT_COMMIT

export JAVA_HOME=/etc/alternatives/jre_1.7.0

sudo yum install -y ccache

cd /home/vagrant/hootenanny-rpms/src/

# Builds and installs necessary RPMs for archiving hoot
rm -f RPMS/x86_64/hoot*.rpm
make -j $((`nproc` + 2)) hoot-deps

cd /home/vagrant/hootenanny-rpms
mkdir -p tmp
cd tmp

[ -e hootenanny ] || git clone https://github.com/ngageoint/hootenanny.git
cd hootenanny
git fetch
git reset
git submodule update --init --recursive
# Clean sometimes refuses to delete these directories. Odd.
rm -rf docs/node_modules hoot-core/tmp/ hoot-core-test/tmp tgs/tmp
git clean -d -f -f -x || echo "It is ok if this fails, it sometimes mysteriously doesn't clean"
git checkout $GIT_COMMIT
# Do a pull just in case a branch was specified.
git pull || echo "Ignore the failure."
git submodule update --init --recursive
cp LocalConfig.pri.orig LocalConfig.pri
echo "QMAKE_CXX=ccache g++" >> LocalConfig.pri

source SetupEnv.sh

# init and start Postgres
PG_VERSION=9.2
sudo service postgresql-$PG_VERSION initdb
sudo service postgresql-$PG_VERSION start
# set Postgres to autostart
sudo /sbin/chkconfig --add postgresql-$PG_VERSION
sudo /sbin/chkconfig postgresql-$PG_VERSION on
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
    sudo /etc/init.d/postgresql-$PG_VERSION restart
fi

# Configure makefiles, we aren't testing services with RPMs yet.
aclocal && autoconf && autoheader && automake && ./configure -q --with-rnd --with-services

# Use the default database
cp conf/DatabaseConfig.sh.orig conf/DatabaseConfig.sh
make -s clean

# Remove any old archives
rm -f hootenanny-*.tar.gz hootenanny-services-*.war
rm -f /home/vagrant/hootenanny-rpms/src/SOURCES/hootenanny-*.tar.gz
rm -f /home/vagrant/hootenanny-rpms/src/SOURCES/hootenanny-services*.war

[ -e /tmp/words1.sqlite ] && cp /tmp/words1.sqlite conf/
make -s -j `nproc`
make -s -j `nproc` archive

# Run the tests that are known to be good on CentOS with a generous timeout
timeout 600s HootTest --exclude=.*RubberSheetConflateTest.sh --exclude=.*ConflateCmdHighwayExactMatchInputsTest.sh --slow

cp -l hootenanny-[0-9]*.tar.gz /home/vagrant/hootenanny-rpms/src/SOURCES/
cp -l hootenanny-services*.war /home/vagrant/hootenanny-rpms/src/SOURCES/
