#!/bin/bash
set -e

## Get variables.
SCRIPT_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $SCRIPT_HOME/Vars.sh

mkdir -p $RPMS

## Build base images.

# Base image that has basic development, RPM authoring, and
# a non-privileged user for building spec files.
docker build \
       --build-arg rpmbuild_dist=$RPMBUILD_DIST \
       --build-arg rpmbuild_uid=$(id -u) \
       -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-base \
       -t hoot/rpmbuild-base \
       $SCRIPT_HOME

# Generic image for building RPMS without any other prerequisites.
docker build \
       -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-generic \
       -t hoot/rpmbuild-generic \
       $SCRIPT_HOME

# Base image with PostgreSQL develop libraries from PGDG at the
# requested version.
docker build \
       --build-arg pg_version=$PG_VERSION \
       -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-pgdg \
       -t hoot/rpmbuild-pgdg:$PG_VERSION \
       $SCRIPT_HOME

## Build GDAL dependencies.

# FileGDBAPI
if [ ! -f $RPM_X86_64/$FILEGDBAPI_RPM ]; then
    echo "#### Building RPM: FileGDBAPI"
    docker run \
           -v $SOURCES:/rpmbuild/SOURCES:ro \
           -v $SPECS:/rpmbuild/SPECS:ro \
           -v $RPMS:/rpmbuild/RPMS:rw \
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
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-generic \
           -t hoot/rpmbuild-geos \
           $SCRIPT_HOME

    # Generate GEOS RPM.
    docker run \
           -v $SOURCES:/rpmbuild/SOURCES:ro \
           -v $SPECS:/rpmbuild/SPECS:ro \
           -v $RPMS:/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-geos \
           rpmbuild -bb SPECS/geos.spec
fi

# libgeotiff
if [ ! -f $RPM_X86_64/$LIBGEOTIFF_RPM ]; then
    echo "#### Building RPM: libgeotiff"

    # Build image for building libgeotiff.
    docker build \
           --build-arg "packages=$( spec_requires libgeotiff )" \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-generic \
           -t hoot/rpmbuild-libgeotiff \
           $SCRIPT_HOME

    # Generate libgeotiff RPM.
    docker run \
           -v $SOURCES:/rpmbuild/SOURCES:ro \
           -v $SPECS:/rpmbuild/SPECS:ro \
           -v $RPMS:/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-libgeotiff \
           rpmbuild -bb SPECS/libgeotiff.spec
fi

# libkml
if [ ! -f $RPM_X86_64/$LIBKML_RPM ]; then
    echo "#### Building RPM: libkml"

    # Build image for building libkml.
    docker build \
           --build-arg "packages=$( spec_requires libkml )" \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-generic \
           -t hoot/rpmbuild-libkml \
           $SCRIPT_HOME

    # Generate libkml RPM.
    docker run \
           -v $SOURCES:/rpmbuild/SOURCES:ro \
           -v $SPECS:/rpmbuild/SPECS:ro \
           -v $RPMS:/rpmbuild/RPMS:rw \
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
           --build-arg "packages=$( spec_requires hoot-gdal )" \
           --build-arg filegdbapi_version=$FILEGDBAPI_VERSION-$FILEGDBAPI_RELEASE \
           --build-arg geos_version=$GEOS_VERSION-$GEOS_RELEASE \
           --build-arg libgeotiff_version=$LIBGEOTIFF_VERSION-$LIBGEOTIFF_RELEASE \
           --build-arg libkml_version=$LIBKML_VERSION-$LIBKML_RELEASE \
           --build-arg pg_version=$PG_VERSION \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-gdal \
           -t hoot/rpmbuild-gdal \
           $SCRIPT_HOME

    # Generate GDAL RPM.
    docker run \
           -v $SOURCES:/rpmbuild/SOURCES:ro \
           -v $SPECS:/rpmbuild/SPECS:ro \
           -v $RPMS:/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-gdal \
           rpmbuild -bb SPECS/hoot-gdal.spec
fi

# PostGIS
if [ ! -f $RPM_X86_64/$POSTGIS_RPM ]; then
    echo "#### Building RPM: PostGIS"

    docker build \
           --build-arg "packages=$( spec_requires hoot-postgis23 )" \
           --build-arg gdal_version=$GDAL_VERSION-$GDAL_RELEASE \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-postgis \
           -t hoot/rpmbuild-postgis \
           $SCRIPT_HOME

    docker run \
           -v $SOURCES:/rpmbuild/SOURCES:ro \
           -v $SPECS:/rpmbuild/SPECS:ro \
           -v $RPMS:/rpmbuild/RPMS:rw \
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
           -v $SPECS:/rpmbuild/SPECS:ro \
           -v $RPMS:/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-generic \
           rpmbuild -bb SPECS/hoot-words.spec
fi

# osmosis
if [ ! -f $RPM_NOARCH/$OSMOSIS_RPM ]; then
    echo "#### Building RPM: osmosis"

    # Generate osmosis RPM.
    docker run \
           -v $SOURCES:/rpmbuild/SOURCES:ro \
           -v $SPECS:/rpmbuild/SPECS:ro \
           -v $RPMS:/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-generic \
           rpmbuild -bb SPECS/osmosis.spec
fi

# stxxl
if [ ! -f $RPM_X86_64/$STXXL_RPM ]; then
    echo "#### Building RPM: stxxl"

    # Generate stxxl RPM.
    docker run \
           -v $SOURCES:/rpmbuild/SOURCES:ro \
           -v $SPECS:/rpmbuild/SPECS:ro \
           -v $RPMS:/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-generic \
           rpmbuild -bb SPECS/stxxl.spec
fi

# tomcat8
if [ ! -f $RPM_NOARCH/$TOMCAT8_RPM ]; then
    echo "#### Building RPM: tomcat8"

    # Generate tomcat8 RPM.
    docker run \
           -v $SOURCES:/rpmbuild/SOURCES:ro \
           -v $SPECS:/rpmbuild/SPECS:ro \
           -v $RPMS:/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-generic \
           rpmbuild -bb SPECS/tomcat8.spec
fi

# wamerican-insane
if [ ! -f $RPM_NOARCH/$WAMERICAN_RPM ]; then
    echo "#### Building RPM: wamerican-insane"

    # Generate wamerican-insane RPM.
    docker run \
           -v $SOURCES:/rpmbuild/SOURCES:ro \
           -v $SPECS:/rpmbuild/SPECS:ro \
           -v $RPMS:/rpmbuild/RPMS:rw \
           -it --rm \
           hoot/rpmbuild-generic \
           rpmbuild -bb SPECS/wamerican-insane.spec
fi
