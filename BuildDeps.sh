#!/bin/bash

# Build RPM dependencies so we don't have to re-build them each time
#
# Yes, the versions are hardcoded. This can be fixed later.
#

set -e
set -x

cd /home/vagrant/hootenanny-rpms

if  ! rpm -qa | grep --quiet FileGDBAPI; then
    if [ ! -f el7-src/FileGDBAPI-1.5.1-1.el7.x86_64.rpm ]; then
        echo "#### Building RPM: FileGDBAPI"
        pushd src
        make -s RPMS/x86_64/FileGDBAPI-1.5.1-1.el7.x86_64.rpm
        cp RPMS/x86_64/FileGDBAPI-1.5.1-1.el7.x86_64.rpm ../el7-src
        popd
    fi
    echo "  Installing RPM: FileGDBAPI"
    sudo yum install -y el7-src/FileGDBAPI-1.5.1-1.el7.x86_64.rpm
fi

if  ! rpm -qa | grep --quiet stxxl-1.3.1; then
    if [ ! -f el7-src/stxxl-1.3.1-1.el7.x86_64.rpm ]; then
        echo "#### Building RPM: stxxl"
        pushd src
        make -s RPMS/x86_64/stxxl-1.3.1-1.el7.x86_64.rpm
        cp RPMS/x86_64/stxxl-1.3.1-1.el7.x86_64.rpm ../el7-src
        cp RPMS/x86_64/stxxl-devel-1.3.1-1.el7.x86_64.rpm ../el7-src
        popd
    fi
    echo "  Installing RPM: stxxl"
    sudo yum install -y el7-src/stxxl-1.3.1-1.el7.x86_64.rpm el7-src/stxxl-devel-1.3.1-1.el7.x86_64.rpm
fi

if  ! rpm -qa | grep --quiet hoot-words; then
    if [ ! -f el7-src/hoot-words-1.0.0-1.el7.noarch.rpm ]; then
        echo "#### Building RPM: Hootenanny Words"
        pushd src
        make -s RPMS/noarch/hoot-words-1.0.0-1.el7.noarch.rpm
        cp RPMS/noarch/hoot-words-1.0.0-1.el7.noarch.rpm  ../el7-src
        popd
    fi
    echo "  Installing RPM: Hootenanny Words"
    sudo yum install -y el7-src/hoot-words-1.0.0-1.el7.noarch.rpm
fi

if  ! rpm -qa | grep --quiet wamerican-insane; then
    if [ ! -f el7-src/wamerican-insane-7.1-1.el7.noarch.rpm ]; then
        echo "#### Building RPM: American Insane Dictionary"
        pushd src
        make -s RPMS/noarch/wamerican-insane-7.1-1.el7.noarch.rpm
        cp RPMS/noarch/wamerican-insane-7.1-1.el7.noarch.rpm  ../el7-src
        popd
    fi
    echo "  Installing RPM: American Insane Dictionary"
    sudo yum install -y el7-src/wamerican-insane-7.1-1.el7.noarch.rpm
fi

if  ! rpm -qa | grep --quiet osmosis; then
    if [ ! -f el7-src/osmosis-0.46-1.el7.noarch.rpm ]; then
        echo "#### Building RPM: Osmosis"
        pushd src
        make -s RPMS/noarch/osmosis-0.46-1.el7.noarch.rpm
        cp RPMS/noarch/osmosis-0.46-1.el7.noarch.rpm  ../el7-src
        popd
    fi
    echo "  Installing RPM: Osmosis"
    sudo yum install -y el7-src/osmosis-0.46-1.el7.noarch.rpm
fi

if  ! rpm -qa | grep --quiet tomcat8; then
    if [ ! -f el7-src/tomcat8-8.5.23-1.el7.noarch.rpm ]; then
        echo "#### Building RPM: Tomcat8"
        pushd src
        make -s RPMS/noarch/tomcat8-8.5.23-1.el7.noarch.rpm
        cp  RPMS/noarch/tomcat8-8.5.23-1.el7.noarch.rpm ../el7-src
        popd
    fi
    echo "  Installing RPM: Tomcat8"
    sudo yum install -y el7-src/tomcat8-8.5.23-1.el7.noarch.rpm
fi

if  ! rpm -qa | grep --quiet hoot-gdal; then
    if [ ! -f el7-src/hoot-gdal-2.1.4-1.el7.x86_64.rpm ]; then
        echo "#### Building RPM: GDAL"
        pushd src
        make -s RPMS/x86_64/hoot-gdal-2.1.4-1.el7.x86_64.rpm
        cp  RPMS/x86_64/hoot-gdal-* ../el7-src
        # Save space
        rm ../el7-src/hoot-gdal-debuginfo-2.1.4-1.el7.x86_64.rpm
        popd
    fi
    echo "  Installing RPM: GDAL"
    sudo yum install -y el7-src/hoot-gdal-*
fi

if  ! rpm -qa | grep --quiet hoot-postgis; then
    if [ ! -f el7-src/hoot-postgis23_95-2.3.4-1.el7.x86_64.rpm ]; then
        echo "#### Building RPM: hoot-postgis"
        pushd src
        make -s RPMS/x86_64/hoot-postgis23_95-2.3.4-1.el7.x86_64.rpm
        cp  RPMS/x86_64/hoot-postgis23_95-* ../el7-src
        rm ../el7-src/hoot-postgis23_95-debuginfo-2.3.4-1.el7.x86_64.rpm
        popd
    fi
    echo "  Installing RPM: PostGIS"
    sudo yum install -y el7-src/hoot-postgis23_95-*
fi
