#!/bin/bash
set -e

## Script location and utility functions.

SCRIPT_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get version from spec file.
function get_version() {
    cat $SCRIPT_HOME/src/SPECS/$1.spec | grep '^Version:[[:space:]]\+[[:digit:]]' | awk '{ print $2 }'
}

# Get release number from spec file.
function get_release() {
    cat $SCRIPT_HOME/src/SPECS/$1.spec | grep '^Release:' | awk '{ gsub(/[^0-9]/, "", $2); print $2 }'
}

# Get build requirement packages from spec file.
function get_requires() {
    # Note: This does not respect `BuildRequires` statements within conditional
    #       macro statements nor version specifiers.
    cat $SCRIPT_HOME/src/SPECS/$1.spec | grep '^BuildRequires:' | awk '{ for (i = 2; i <= NF; ++i) if ($i ~ /^[[:alpha:]]/ && $i !~ /[\%\{\}]/) print $i }' ORS=' '
}


## Package versioning variables.

# Important: Hootenanny and PostgreSQL depend on this.
PG_VERSION=9.5
PG_DOTLESS=$(echo $PG_VERSION | tr -d '.')

FILEGDBAPI_VERSION=$( get_version FileGDBAPI )
FILEGDBAPI_RELEASE=$( get_release FileGDBAPI )
FILEGDBAPI_RPM=FileGDBAPI-$FILEGDBAPI_VERSION-$FILEGDBAPI_RELEASE.el7.x86_64.rpm

GDAL_VERSION=$( get_version hoot-gdal )
GDAL_RELEASE=$( get_release hoot-gdal )
GDAL_RPM_SUFFIX=$GDAL_VERSION-$GDAL_RELEASE.el7.x86_64.rpm
GDAL_RPM=hoot-gdal-$GDAL_RPM_SUFFIX

GEOS_VERSION=$( get_version geos )
GEOS_RELEASE=$( get_release geos )
GEOS_RPM=geos-$GEOS_VERSION-$GEOS_RELEASE.el7.x86_64.rpm
GEOS_DEVEL_RPM=geos-devel-$GEOS_VERSION-$GEOS_RELEASE.el7.x86_64.rpm

LIBGEOTIFF_VERSION=$( get_version libgeotiff )
LIBGEOTIFF_RELEASE=$( get_release libgeotiff )
LIBGEOTIFF_RPM=libgeotiff-$LIBGEOTIFF_VERSION-$LIBGEOTIFF_RELEASE.el7.x86_64.rpm
LIBGEOTIFF_DEVEL_RPM=libgeotiff-devel-$LIBGEOTIFF_VERSION-$LIBGEOTIFF_RELEASE.el7.x86_64.rpm

LIBKML_VERSION=$( get_version libkml )
LIBKML_RELEASE=$( get_release libkml )
LIBKML_RPM=libkml-$LIBKML_VERSION-$LIBKML_RELEASE.el7.x86_64.rpm
LIBKML_DEVEL_RPM=libkml-devel-$LIBKML_VERSION-$LIBKML_RELEASE.el7.x86_64.rpm

OSMOSIS_VERSION=$( get_version osmosis )
OSMOSIS_RELEASE=$( get_release osmosis )
OSMOSIS_RPM=osmosis-$OSMOSIS_VERSION-$OSMOSIS_RELEASE.el7.noarch.rpm

POSTGIS_VERSION=$( get_version hoot-postgis23 )
POSTGIS_RELEASE=$( get_release hoot-postgis23)
POSTGIS_RPM=hoot-postgis23_$PG_DOTLESS-$POSTGIS_VERSION-$POSTGIS_RELEASE.el7.x86_64.rpm

STXXL_VERSION=$( get_version stxxl )
STXXL_RELEASE=$( get_release stxxl )
STXXL_RPM=stxxl-$STXXL_VERSION-$STXXL_RELEASE.el7.x86_64.rpm
STXXL_DEVEL_RPM=stxxl-devel-$STXXL_VERSION-$STXXL_RELEASE.el7.x86_64.rpm

TOMCAT8_VERSION=$( get_version tomcat8 )
TOMCAT8_RELEASE=$( get_release tomcat8 )
TOMCAT8_RPM=tomcat8-$TOMCAT8_VERSION-$TOMCAT8_RELEASE.el7.noarch.rpm

WAMERICAN_VERSION=$( get_version wamerican-insane )
WAMERICAN_RELEASE=$( get_release wamerican-insane )
WAMERICAN_RPM=wamerican-insane-$WAMERICAN_VERSION-$WAMERICAN_RELEASE.el7.noarch.rpm

WORDS_VERSION=$( get_version hoot-words )
WORDS_RELEASE=$( get_release hoot-words )
WORDS_RPM=hoot-words-$WORDS_VERSION-$WORDS_RELEASE.el7.noarch.rpm


## Build base images.

# Base image that has basic development, RPM authoring, and
# a non-privileged user for building spec files.
docker build \
       --build-arg rpmbuild_uid=$(id -u) \
       -t hoot/rpmbuild-base \
       $SCRIPT_HOME/deps/base

# Generic image for building RPMS without any other prerequisites.
docker build \
       -t hoot/rpmbuild-generic \
       $SCRIPT_HOME/deps/generic

# Base image with PostgreSQL develop libraries from PGDG at the
# requested version.
docker build \
       --build-arg pg_version=$PG_VERSION \
       -t hoot/rpmbuild-pgdg:$PG_VERSION \
       $SCRIPT_HOME/deps/pgdg

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
           rpmbuild -bb SPECS/FileGDBAPI.spec
    cp $SCRIPT_HOME/src/RPMS/x86_64/$FILEGDBAPI_RPM $SCRIPT_HOME/el7-src
fi

# GEOS
if [ ! -f $SCRIPT_HOME/el7-src/$GEOS_RPM ]; then
    echo "#### Building RPM: GEOS"

    # Build image for building GEOS.
    docker build \
           --build-arg packages=doxygen \
           -t hoot/rpmbuild-geos \
           $SCRIPT_HOME/deps/generic

    # Generate GEOS RPM.
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-geos \
           rpmbuild -bb SPECS/geos.spec
    cp $SCRIPT_HOME/src/RPMS/x86_64/{$GEOS_RPM,$GEOS_DEVEL_RPM} $SCRIPT_HOME/el7-src
fi

# libgeotiff
if [ ! -f $SCRIPT_HOME/el7-src/$LIBGEOTIFF_RPM ]; then
    echo "#### Building RPM: libgeotiff"

    # Build image for building libgeotiff.
    docker build \
           --build-arg "packages=$( get_requires libgeotiff )" \
           -t hoot/rpmbuild-libgeotiff \
           $SCRIPT_HOME/deps/generic

    # Generate libgeotiff RPM.
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-libgeotiff \
           rpmbuild -bb SPECS/libgeotiff.spec
    cp $SCRIPT_HOME/src/RPMS/x86_64/{$LIBGEOTIFF_RPM,$LIBGEOTIFF_DEVEL_RPM} $SCRIPT_HOME/el7-src
fi

# libkml
if [ ! -f $SCRIPT_HOME/el7-src/$LIBKML_RPM ]; then
    echo "#### Building RPM: libkml"

    # Build image for building libkml.
    docker build \
           --build-arg "packages=$( get_requires libkml )" \
           -t hoot/rpmbuild-libkml \
           $SCRIPT_HOME/deps/generic

    # Generate libkml RPM.
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-libkml \
           rpmbuild -bb SPECS/libkml.spec
    cp $SCRIPT_HOME/src/RPMS/x86_64/{$LIBKML_RPM,$LIBKML_DEVEL_RPM} $SCRIPT_HOME/el7-src
fi

## GDAL and PostGIS (requires PostgreSQL from PGDG)

# GDAL
if [ ! -f $SCRIPT_HOME/el7-src/$GDAL_RPM ]; then
    echo "#### Building RPM: GDAL (with PostgreSQL ${PG_VERSION})"

    # Copy in dependency RPMs into GDAL container's folder.
    cp $SCRIPT_HOME/src/RPMS/x86_64/{$FILEGDBAPI_RPM,$GEOS_RPM,$GEOS_DEVEL_RPM,$LIBGEOTIFF_RPM,$LIBGEOTIFF_DEVEL_RPM,$LIBKML_RPM,$LIBKML_DEVEL_RPM} \
       $SCRIPT_HOME/deps/gdal

    # Make GDAL RPM container, specifying the versions of RPMs we
    # need to install.
    docker build \
           --build-arg "packages=$( get_requires hoot-gdal )" \
           --build-arg filegdbapi_version=$FILEGDBAPI_VERSION-$FILEGDBAPI_RELEASE \
           --build-arg geos_version=$GEOS_VERSION-$GEOS_RELEASE \
           --build-arg libgeotiff_version=$LIBGEOTIFF_VERSION-$LIBGEOTIFF_RELEASE \
           --build-arg libkml_version=$LIBKML_VERSION-$LIBKML_RELEASE \
           --build-arg pg_version=$PG_VERSION \
           -t hoot/rpmbuild-gdal \
           $SCRIPT_HOME/deps/gdal

    # Cleanup dependency RPMs.
    rm -f $SCRIPT_HOME/deps/gdal/*.rpm

    # Generate GDAL RPM.
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-gdal \
           rpmbuild -bb SPECS/hoot-gdal.spec
    cp $SCRIPT_HOME/src/RPMS/x86_64/$GDAL_RPM \
       $SCRIPT_HOME/src/RPMS/x86_64/hoot-gdal-devel-$GDAL_RPM_SUFFIX \
       $SCRIPT_HOME/src/RPMS/x86_64/hoot-gdal-java-$GDAL_RPM_SUFFIX \
       $SCRIPT_HOME/src/RPMS/x86_64/hoot-gdal-libs-$GDAL_RPM_SUFFIX \
       $SCRIPT_HOME/src/RPMS/x86_64/hoot-gdal-perl-$GDAL_RPM_SUFFIX \
       $SCRIPT_HOME/src/RPMS/x86_64/hoot-gdal-python-$GDAL_RPM_SUFFIX \
       $SCRIPT_HOME/src/RPMS/x86_64/hoot-gdal-python3-$GDAL_RPM_SUFFIX \
       $SCRIPT_HOME/el7-src
fi

# PostGIS
if [ ! -f $SCRIPT_HOME/el7-src/$POSTGIS_RPM ]; then
    echo "#### Building RPM: PostGIS"

    cp $SCRIPT_HOME/src/RPMS/x86_64/$GDAL_RPM \
       $SCRIPT_HOME/src/RPMS/x86_64/hoot-gdal-devel-$GDAL_RPM_SUFFIX \
       $SCRIPT_HOME/src/RPMS/x86_64/hoot-gdal-libs-$GDAL_RPM_SUFFIX \
       $SCRIPT_HOME/deps/postgis

    docker build \
           --build-arg "packages=$( get_requires hoot-postgis23 )" \
           --build-arg gdal_version=$GDAL_VERSION-$GDAL_RELEASE \
           -t hoot/rpmbuild-postgis \
           $SCRIPT_HOME/deps/postgis

    # Cleanup dependency RPMs.
    rm -f $SCRIPT_HOME/deps/postgis/*.rpm

    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-postgis \
           rpmbuild -bb SPECS/hoot-postgis23.spec

    cp $SCRIPT_HOME/src/RPMS/x86_64/hoot-postgis23*.rpm \
       $SCRIPT_HOME/el7-src
fi

## Simple Dependencies

# hoot-words
if [ ! -f $SCRIPT_HOME/el7-src/$WORDS_RPM ]; then
    echo "#### Building RPM: hoot-words"

    # Generate hoot-words RPM (do not share SOURCES directory, as
    # it's a forced download from spec file).
    docker run \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-generic \
           rpmbuild -bb SPECS/hoot-words.spec
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
           rpmbuild -bb SPECS/osmosis.spec
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
           rpmbuild -bb SPECS/stxxl.spec
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
           rpmbuild -bb SPECS/tomcat8.spec
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
           rpmbuild -bb SPECS/wamerican-insane.spec
    cp $SCRIPT_HOME/src/RPMS/noarch/$WAMERICAN_RPM $SCRIPT_HOME/el7-src
fi
