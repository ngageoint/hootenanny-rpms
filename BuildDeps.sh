#!/bin/bash
set -e

## Variables

SCRIPT_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

GEOS_VERSION=$(cat $SCRIPT_HOME/src/SPECS/geos.spec | grep '^Version:[[:space:]]\+[[:digit:]]' | awk '{ print $2 }')
GEOS_RELEASE=$(cat $SCRIPT_HOME/src/SPECS/geos.spec | grep '^Release:' | awk '{ gsub(/[^0-9]/, "", $2); print $2 }')
GEOS_RPM=geos-$GEOS_VERSION-$GEOS_RELEASE.el7.x86_64.rpm
GEOS_DEVEL_RPM=geos-devel-$GEOS_VERSION-$GEOS_RELEASE.el7.x86_64.rpm

FILEGDBAPI_VERSION=$(cat $SCRIPT_HOME/src/SPECS/FileGDBAPI.spec | grep '^Version:[[:space:]]\+[[:digit:]]' | awk '{ print $2 }')
FILEGDBAPI_RELEASE=$(cat $SCRIPT_HOME/src/SPECS/FileGDBAPI.spec | grep '^Release:' | awk '{ gsub(/[^0-9]/, "", $2); print $2 }')
FILEGDBAPI_RPM=FileGDBAPI-$FILEGDBAPI_VERSION-$FILEGDBAPI_RELEASE.el7.x86_64.rpm

LIBGEOTIFF_VERSION=$(cat $SCRIPT_HOME/src/SPECS/libgeotiff.spec | grep '^Version:[[:space:]]\+[[:digit:]]' | awk '{ print $2 }')
LIBGEOTIFF_RELEASE=$(cat $SCRIPT_HOME/src/SPECS/libgeotiff.spec | grep '^Release:' | awk '{ gsub(/[^0-9]/, "", $2); print $2 }')
LIBGEOTIFF_RPM=libgeotiff-$LIBGEOTIFF_VERSION-$LIBGEOTIFF_RELEASE.el7.x86_64.rpm
LIBGEOTIFF_DEVEL_RPM=libgeotiff-devel-$LIBGEOTIFF_VERSION-$LIBGEOTIFF_RELEASE.el7.x86_64.rpm

LIBKML_VERSION=$(cat $SCRIPT_HOME/src/SPECS/libkml.spec | grep '^Version:[[:space:]]\+[[:digit:]]' | awk '{ print $2 }')
LIBKML_RELEASE=$(cat $SCRIPT_HOME/src/SPECS/libkml.spec | grep '^Release:' | awk '{ gsub(/[^0-9]/, "", $2); print $2 }')
LIBKML_RPM=libkml-$LIBKML_VERSION-$LIBKML_RELEASE.el7.x86_64.rpm
LIBKML_DEVEL_RPM=libkml-devel-$LIBKML_VERSION-$LIBKML_RELEASE.el7.x86_64.rpm

OSMOSIS_VERSION=$(cat $SCRIPT_HOME/src/SPECS/osmosis.spec | grep '^Version:[[:space:]]\+[[:digit:]]' | awk '{ print $2 }')
OSMOSIS_RELEASE=$(cat $SCRIPT_HOME/src/SPECS/osmosis.spec | grep '^Release:' | awk '{ gsub(/[^0-9]/, "", $2); print $2 }')
OSMOSIS_RPM=osmosis-$OSMOSIS_VERSION-$OSMOSIS_RELEASE.el7.noarch.rpm

STXXL_VERSION=$(cat $SCRIPT_HOME/src/SPECS/stxxl.spec | grep '^Version:[[:space:]]\+[[:digit:]]' | awk '{ print $2 }')
STXXL_RELEASE=$(cat $SCRIPT_HOME/src/SPECS/stxxl.spec | grep '^Release:' | awk '{ gsub(/[^0-9]/, "", $2); print $2 }')
STXXL_RPM=stxxl-$STXXL_VERSION-$STXXL_RELEASE.el7.x86_64.rpm
STXXL_DEVEL_RPM=stxxl-devel-$STXXL_VERSION-$STXXL_RELEASE.el7.x86_64.rpm

TOMCAT8_VERSION=$(cat $SCRIPT_HOME/src/SPECS/tomcat8.spec | grep '^Version:[[:space:]]\+[[:digit:]]' | awk '{ print $2 }')
TOMCAT8_RELEASE=$(cat $SCRIPT_HOME/src/SPECS/tomcat8.spec | grep '^Release:' | awk '{ gsub(/[^0-9]/, "", $2); print $2 }')
TOMCAT8_RPM=tomcat8-$TOMCAT8_VERSION-$TOMCAT8_RELEASE.el7.noarch.rpm

WAMERICAN_VERSION=$(cat $SCRIPT_HOME/src/SPECS/wamerican-insane.spec | grep '^Version:[[:space:]]\+[[:digit:]]' | awk '{ print $2 }')
WAMERICAN_RELEASE=$(cat $SCRIPT_HOME/src/SPECS/wamerican-insane.spec | grep '^Release:' | awk '{ gsub(/[^0-9]/, "", $2); print $2 }')
WAMERICAN_RPM=wamerican-insane-$WAMERICAN_VERSION-$WAMERICAN_RELEASE.el7.noarch.rpm

WORDS_VERSION=$(cat $SCRIPT_HOME/src/SPECS/hoot-words.spec | grep '^Version:[[:space:]]\+[[:digit:]]' | awk '{ print $2 }')
WORDS_RELEASE=$(cat $SCRIPT_HOME/src/SPECS/hoot-words.spec | grep '^Release:' | awk '{ gsub(/[^0-9]/, "", $2); print $2 }')
WORDS_RPM=hoot-words-$WORDS_VERSION-$WORDS_RELEASE.el7.noarch.rpm


# Important: Hootenanny and PostgreSQL depend on this.
POSTGRES_VERSION=9.5

## Build base images.

docker build -t hoot/rpmbuild-base $SCRIPT_HOME/deps/base
docker build -t hoot/rpmbuild-generic $SCRIPT_HOME/deps/generic
docker build --build-arg pg_version=$POSTGRES_VERSION -t hoot/rpmbuild-pgdg$POSTGRES_VERSION $SCRIPT_HOME/deps/pgdg

## Build GDAL dependencies.

# FileGDBAPI
if [ ! -f $SCRIPT_HOME/el7-src/$FILEGDBAPI_RPM ]; then
    echo "#### Building RPM: FileGDBAPI"
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-generic \
           rpmbuild -ba SPECS/FileGDBAPI.spec
    cp $SCRIPT_HOME/src/RPMS/x86_64/$FILEGDBAPI_RPM $SCRIPT_HOME/el7-src
fi

# GEOS
if [ ! -f $SCRIPT_HOME/el7-src/$GEOS_RPM ]; then
    echo "#### Building RPM: GEOS"

    # Build image for building GEOS.
    docker build \
           --build-arg "packages=doxygen" \
           -t hoot/rpmbuild-geos \
           $SCRIPT_HOME/deps/generic

    # Generate GEOS RPM.
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-geos \
           rpmbuild -ba SPECS/geos.spec
    cp $SCRIPT_HOME/src/RPMS/x86_64/{$GEOS_RPM,$GEOS_DEVEL_RPM} $SCRIPT_HOME/el7-src
fi

# libgeotiff
if [ ! -f $SCRIPT_HOME/el7-src/$LIBGEOTIFF_RPM ]; then
    echo "#### Building RPM: libgeotiff"
    LIBGEOTIFF_REQUIRES=$(cat $SCRIPT_HOME/src/SPECS/libgeotiff.spec | grep '^BuildRequires:' | awk '{ for (i = 2; i <= NF; ++i) if ($i ~ /^[[:alpha:]]/ && $i !~ /[\%\{\}]/) print $i }' ORS=" ")

    # Build image for building libgeotiff.
    docker build \
           --build-arg "packages=${LIBGEOTIFF_REQUIRES}" \
           -t hoot/rpmbuild-libgeotiff \
           $SCRIPT_HOME/deps/generic

    # Generate libgeotiff RPM.
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-libgeotiff \
           rpmbuild -ba SPECS/libgeotiff.spec
    cp $SCRIPT_HOME/src/RPMS/x86_64/{$LIBGEOTIFF_RPM,$LIBGEOTIFF_DEVEL_RPM} $SCRIPT_HOME/el7-src
fi

# libkml
if [ ! -f $SCRIPT_HOME/el7-src/$LIBKML_RPM ]; then
    echo "#### Building RPM: libkml"
    LIBKML_REQUIRES=$(cat $SCRIPT_HOME/src/SPECS/libkml.spec | grep '^BuildRequires:' | awk '{ for (i = 2; i <= NF; ++i) if ($i ~ /^[[:alpha:]]/ && $i !~ /[\%\{\}]/) print $i }' ORS=" ")

    # Build image for building libkml.
    docker build \
           --build-arg "packages=${LIBKML_REQUIRES}" \
           -t hoot/rpmbuild-libkml \
           $SCRIPT_HOME/deps/generic

    # Generate libkml RPM.
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-libkml \
           rpmbuild -ba SPECS/libkml.spec
    cp $SCRIPT_HOME/src/RPMS/x86_64/{$LIBKML_RPM,$LIBKML_DEVEL_RPM} $SCRIPT_HOME/el7-src
fi


## Simple Dependencies

# hoot-words
if [ ! -f $SCRIPT_HOME/el7-src/$WORDS_RPM ]; then
    echo "#### Building RPM: hoot-words"

    # Generate hoot-words RPM (do not share SOURCES directory, as
    # it's forced download from spec file).
    docker run \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-generic \
           rpmbuild -ba SPECS/hoot-words.spec
    cp $SCRIPT_HOME/src/RPMS/noarch/$WORDS_RPM $SCRIPT_HOME/el7-src
fi

# osmosis
if [ ! -f $SCRIPT_HOME/el7-src/$OSMOSIS_RPM ]; then
    echo "#### Building RPM: osmosis"

    # Generate osmosis RPM.
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-generic \
           rpmbuild -ba SPECS/osmosis.spec
    cp $SCRIPT_HOME/src/RPMS/noarch/$OSMOSIS_RPM $SCRIPT_HOME/el7-src
fi

# stxxl
if [ ! -f $SCRIPT_HOME/el7-src/$STXXL_RPM ]; then
    echo "#### Building RPM: stxxl"

    # Generate stxxl RPM.
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-generic \
           rpmbuild -ba SPECS/stxxl.spec
    cp $SCRIPT_HOME/src/RPMS/x86_64/{$STXXL_RPM,$STXXL_DEVEL_RPM} $SCRIPT_HOME/el7-src
fi

# tomcat8
if [ ! -f $SCRIPT_HOME/el7-src/$TOMCAT8_RPM ]; then
    echo "#### Building RPM: tomcat8"

    # Generate tomcat8 RPM.
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-generic \
           rpmbuild -ba SPECS/tomcat8.spec
    cp $SCRIPT_HOME/src/RPMS/noarch/$TOMCAT8_RPM $SCRIPT_HOME/el7-src
fi

# wamerican-insane
if [ ! -f $SCRIPT_HOME/el7-src/$WAMERICAN_RPM ]; then
    echo "#### Building RPM: wamerican-insane"

    # Generate wamerican-insane RPM.
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-generic \
           rpmbuild -ba SPECS/wamerican-insane.spec
    cp $SCRIPT_HOME/src/RPMS/noarch/$WAMERICAN_RPM $SCRIPT_HOME/el7-src
fi
