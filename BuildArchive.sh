#!/bin/bash

# Used by the makefile to build a hoot tar ball on vagrant

set -e
set -x

echo $GIT_COMMIT

sudo yum install -y ccache

cd /home/vagrant/hootenanny-rpms/src/

# Builds and installs necessary RPMs for archiving hoot
# -j seems to cause errors -- fix another time...
#make -s -j `grep -c ^processor /proc/cpuinfo` hoot-deps
rm -f RPMS/x86_64/hoot*.rpm
make hoot-deps

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
cp LocalConfig.pri.orig LocalConfig.pri
echo "QMAKE_CXX=ccache g++" >> LocalConfig.pri

source SetupEnv.sh

# Configure makefiles, we aren't testing services with RPMs yet.
aclocal && autoconf && autoheader && automake && ./configure -q --with-rnd --with-services

# Use the default database
cp conf/DatabaseConfig.sh.orig conf/DatabaseConfig.sh
make -s clean

# Remove any old archives
rm -f hootenanny-*.tar.gz hootenanny-services-*.war
rm -f /home/vagrant/hootenanny-rpms/src/SOURCES/hootenanny-*.tar.gz

[ -e /tmp/words1.sqlite ] && cp /tmp/words1.sqlite conf/
make -s -j `grep -c ^processor /proc/cpuinfo`
make -s -j `grep -c ^processor /proc/cpuinfo` archive

# Run the tests that are known to be good on CentOS with a generous timeout
timeout 600s HootTest --exclude=.*RubberSheetConflateTest.sh --exclude=.*ConflateCmdHighwayExactMatchInputsTest.sh --slow

cp -l hootenanny-*.tar.gz /home/vagrant/hootenanny-rpms/src/SOURCES/

