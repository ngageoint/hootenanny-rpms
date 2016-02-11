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
git reset
# Clean sometimes refuses to delete these directories. Odd.
rm -rf docs/node_modules hoot-core/tmp/
git clean -d -f -f -x
git checkout $GIT_COMMIT
cp LocalConfig.pri.orig LocalConfig.pri
echo "QMAKE_CXX=ccache g++" >> LocalConfig.pri

source SetupEnv.sh

# Configure makefiles, we aren't testing services with RPMs yet.
aclocal && autoconf && autoheader && automake && ./configure -q --with-rnd

# Use the default database
cp conf/DatabaseConfig.sh.orig conf/DatabaseConfig.sh
make -s -j `grep -c ^processor /proc/cpuinfo` archive

# Run the tests that are known to be good on CentOS with a generous timeout
timeout 600s HootTest --exclude=.*RubberSheetConflateTest.sh --exclude=.*ConflateCmdHighwayExactMatchInputsTest.sh --slow

# old archives shouldn't exist, but make sure they aren't there
rm -f hootenanny-*.tar.gz hootenanny-services-*.war

# These might exist
rm -f /home/vagrant/hootenanny-rpms/src/SOURCES/hootenanny-*.tar.gz

make -sj2 archive

cp -l hootenanny-*.tar.gz /home/vagrant/hootenanny-rpms/src/SOURCES/

