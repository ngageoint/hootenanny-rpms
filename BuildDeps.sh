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

# Where binary RPMs are placed.
RPM_X86_64=$SCRIPT_HOME/src/RPMS/x86_64
RPM_NOARCH=$SCRIPT_HOME/src/RPMS/noarch

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
POSTGIS_RELEASE=$( get_release hoot-postgis23 )
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
       -f $SCRIPT_HOME/docker/base/Dockerfile \
       -t hoot/rpmbuild-base \
       $SCRIPT_HOME

# Generic image for building RPMS without any other prerequisites.
docker build \
       -f $SCRIPT_HOME/docker/generic/Dockerfile \
       -t hoot/rpmbuild-generic \
       $SCRIPT_HOME

# Base image with PostgreSQL develop libraries from PGDG at the
# requested version.
docker build \
       --build-arg pg_version=$PG_VERSION \
       -f $SCRIPT_HOME/docker/pgdg/Dockerfile \
       -t hoot/rpmbuild-pgdg:$PG_VERSION \
       $SCRIPT_HOME

## Build GDAL dependencies.

# FileGDBAPI
if [ ! -f $RPM_X86_64/$FILEGDBAPI_RPM ]; then
    echo "#### Building RPM: FileGDBAPI"
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-generic \
           rpmbuild -bb SPECS/FileGDBAPI.spec
fi

# GEOS
if [ ! -f $RPM_X86_64/$GEOS_RPM ]; then
    echo "#### Building RPM: GEOS"

    # Build image for building GEOS.
    docker build \
           --build-arg packages=doxygen \
           -f $SCRIPT_HOME/docker/generic/Dockerfile \
           -t hoot/rpmbuild-geos \
           $SCRIPT_HOME

    # Generate GEOS RPM.
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-geos \
           rpmbuild -bb SPECS/geos.spec
fi

# libgeotiff
if [ ! -f $RPM_X86_64/$LIBGEOTIFF_RPM ]; then
    echo "#### Building RPM: libgeotiff"

    # Build image for building libgeotiff.
    docker build \
           --build-arg "packages=$( get_requires libgeotiff )" \
           -f $SCRIPT_HOME/docker/generic/Dockerfile \
           -t hoot/rpmbuild-libgeotiff \
           $SCRIPT_HOME

    # Generate libgeotiff RPM.
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-libgeotiff \
           rpmbuild -bb SPECS/libgeotiff.spec
fi

# libkml
if [ ! -f $RPM_X86_64/$LIBKML_RPM ]; then
    echo "#### Building RPM: libkml"

    # Build image for building libkml.
    docker build \
           --build-arg "packages=$( get_requires libkml )" \
           -f $SCRIPT_HOME/docker/generic/Dockerfile \
           -t hoot/rpmbuild-libkml \
           $SCRIPT_HOME

    # Generate libkml RPM.
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-libkml \
           rpmbuild -bb SPECS/libkml.spec
fi

## GDAL and PostGIS (requires PostgreSQL from PGDG)

# GDAL
if [ ! -f $RPM_X86_64/$GDAL_RPM ]; then
    echo "#### Building RPM: GDAL (with PostgreSQL ${PG_VERSION})"

    # Make GDAL RPM container, specifying the versions of RPMs we
    # need to install.
    docker build \
           --build-arg "packages=$( get_requires hoot-gdal )" \
           --build-arg filegdbapi_version=$FILEGDBAPI_VERSION-$FILEGDBAPI_RELEASE \
           --build-arg geos_version=$GEOS_VERSION-$GEOS_RELEASE \
           --build-arg libgeotiff_version=$LIBGEOTIFF_VERSION-$LIBGEOTIFF_RELEASE \
           --build-arg libkml_version=$LIBKML_VERSION-$LIBKML_RELEASE \
           --build-arg pg_version=$PG_VERSION \
           -f $SCRIPT_HOME/docker/gdal/Dockerfile \
           -t hoot/rpmbuild-gdal \
           $SCRIPT_HOME

    # Generate GDAL RPM.
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-gdal \
           rpmbuild -bb SPECS/hoot-gdal.spec
fi

# PostGIS
if [ ! -f $RPM_X86_64/$POSTGIS_RPM ]; then
    echo "#### Building RPM: PostGIS"

    docker build \
           --build-arg "packages=$( get_requires hoot-postgis23 )" \
           --build-arg gdal_version=$GDAL_VERSION-$GDAL_RELEASE \
           -f $SCRIPT_HOME/docker/postgis/Dockerfile \
           -t hoot/rpmbuild-postgis \
           $SCRIPT_HOME

    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-postgis \
           rpmbuild -bb SPECS/hoot-postgis23.spec
fi

## Simple Dependencies

# hoot-words
if [ ! -f $RPM_NOARCH/$WORDS_RPM ]; then
    echo "#### Building RPM: hoot-words"

    # Generate hoot-words RPM (do not share SOURCES directory, as
    # it's a forced download from spec file).
    docker run \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-generic \
           rpmbuild -bb SPECS/hoot-words.spec
fi

# osmosis
if [ ! -f $RPM_NOARCH/$OSMOSIS_RPM ]; then
    echo "#### Building RPM: osmosis"

    # Generate osmosis RPM.
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-generic \
           rpmbuild -bb SPECS/osmosis.spec
fi

# stxxl
if [ ! -f $RPM_X86_64/$STXXL_RPM ]; then
    echo "#### Building RPM: stxxl"

    # Generate stxxl RPM.
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-generic \
           rpmbuild -bb SPECS/stxxl.spec
fi

# tomcat8
if [ ! -f $RPM_NOARCH/$TOMCAT8_RPM ]; then
    echo "#### Building RPM: tomcat8"

    # Generate tomcat8 RPM.
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-generic \
           rpmbuild -bb SPECS/tomcat8.spec
fi

# wamerican-insane
if [ ! -f $RPM_NOARCH/$WAMERICAN_RPM ]; then
    echo "#### Building RPM: wamerican-insane"

    # Generate wamerican-insane RPM.
    docker run \
           -v "${SCRIPT_HOME}/src/SOURCES":/rpmbuild/SOURCES:ro \
           -v "${SCRIPT_HOME}/src/SPECS":/rpmbuild/SPECS:ro \
           -v "${SCRIPT_HOME}/src/RPMS":/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-generic \
           rpmbuild -bb SPECS/wamerican-insane.spec
fi
