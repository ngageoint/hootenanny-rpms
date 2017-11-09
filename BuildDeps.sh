#!/bin/bash

# Build RPM dependencies so we don't have to re-build them each time
#
# Yes, the versions are hardcoded. This can be fixed later.
#

set -e
set -x

cd /home/vagrant/hootenanny-rpms

if  ! rpm -qa | grep --quiet FileGDB_API; then
    if [ ! -f el7-src/FileGDB_API-1.5.1-1.el7.centos.x86_64.rpm ]; then
        echo "#### Building RPM: FileGDB_API"
        pushd src
        make -s RPMS/x86_64/FileGDB_API-1.5.1-1.el7.centos.x86_64.rpm
        cp RPMS/x86_64/FileGDB_API-1.5.1-1.el7.centos.x86_64.rpm ../el7-src
        popd
    fi
    echo "  Installing RPM: FileGDB_API"
    sudo yum install -y el7-src/FileGDB_API-1.5.1-1.el7.centos.x86_64.rpm
fi

if  ! rpm -qa | grep --quiet stxxl-1.3.1; then
    if [ ! -f el7-src/stxxl-1.3.1-1.el7.centos.x86_64.rpm ]; then
        echo "#### Building RPM: stxxl"
        pushd src
        make -s RPMS/x86_64/stxxl-1.3.1-1.el7.x86_64.rpm
        cp RPMS/x86_64/stxxl-1.3.1-1.el7.x86_64.rpm ../el7-src
        cp RPMS/x86_64/stxxl-devel-1.3.1-1.el7.centos.x86_64.rpm ../el7-src
        popd
    fi
    echo "  Installing RPM: stxxl"
    sudo yum install -y el7-src/stxxl-1.3.1-1.el7.centos.x86_64.rpm el7-src/stxxl-devel-1.3.1-1.el7.centos.x86_64.rpm
fi

if  ! rpm -qa | grep --quiet hootenanny-words; then
    if [ ! -f el7-src/hootenanny-words-1.0.0-1.noarch.rpm ]; then
        echo "#### Building RPM: Hootenanny Words"
        pushd src
        make -s RPMS/noarch/hootenanny-words-1.0.0-1.noarch.rpm
        cp RPMS/noarch/hootenanny-words-1.0.0-1.noarch.rpm  ../el7-src
        popd
    fi
    echo "  Installing RPM: Hootenanny Words"
    sudo yum install -y el7-src/hootenanny-words-1.0.0-1.noarch.rpm
fi

if  ! rpm -qa | grep --quiet tomcat8; then
    if [ ! -f el7-src/tomcat8-8.5.23-1.noarch.rpm ]; then
        echo "#### Building RPM: Tomcat8"
        pushd src
        make -s RPMS/noarch/tomcat8-8.5.23-1.noarch.rpm
        cp  RPMS/noarch/tomcat8-8.5.23-1.noarch.rpm ../el7-src
        popd
    fi
    echo "  Installing RPM: Tomcat8"
    sudo yum install -y el7-src/tomcat8-8.5.23-1.noarch.rpm
fi

if  ! rpm -qa | grep --quiet gdal-2; then
    if [ ! -f el7-src/gdal-2.1.4-8.el7.centos.x86_64.rpm ]; then
        echo "#### Building RPM: GDAL"
        pushd src
        make -s RPMS/x86_64/gdal-2.1.4-2.el7.x86_64.rpm
        cp  RPMS/x86_64/gdal-* ../el7-src
        # Save space
        rm ../el7-src/gdal-debuginfo-2.1.4-8.el7.centos.x86_64.rpm
        popd
    fi
    echo "  Installing RPM: GDAL"
    sudo yum install -y el7-src/gdal-*
fi

# Not needed since we are building from the main GDAL source code
# if  ! rpm -qa | grep --quiet gdal.x86_64; then
#     if [ ! -f el7-src/gdal-esri-epsg-2.1.4-2.el7.centos.x86_64.rpm ]; then
#         echo "#### Building RPM: GDAL epsg"
#         pushd src
#         make -s  RPMS/x86_64/gdal-esri-epsg-2.1.4-2.el7.centos.x86_64.rpm
#         cp   RPMS/x86_64/gdal-esri-epsg-2.1.4-2.el7.centos.x86_64.rpm ../el7-src
#         popd
#     fi
#     echo "  Installing RPM: GDAL epsg"
#     sudo yum install -y el7-src/gdal-esri-epsg-2.1.4-2.el7.centos.x86_64.rpm
# fi

if  ! rpm -qa | grep --quiet postgis; then
    if [ ! -f el7-src/postgis-2.3.3-3.el7.centos.x86_64.rpm ]; then
        echo "#### Building RPM: postgis"
        pushd src
        make -s RPMS/x86_64/postgis-2.3.3-3.el7.centos.x86_64.rpm
        cp  RPMS/x86_64/postgis-* ../el7-src
        rm ../el7-src/postgis-debuginfo-2.3.3-3.el7.centos.x86_64.rpm
        popd
    fi
    echo "  Installing RPM: Postgis"
    sudo yum install -y el7-src/postgis-*
fi
