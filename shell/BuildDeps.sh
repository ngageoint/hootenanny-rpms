#!/bin/bash
set -euxo pipefail

## Get variables.
source "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/Vars.sh

# Ensure base images are built.
build_base_images

## Build GDAL dependencies.

# FileGDBAPI
if [ ! -f $RPM_X86_64/$FILEGDBAPI_RPM ]; then
    echo "#### Building RPM: FileGDBAPI"
    run_dep_image \
        rpmbuild \
        --define "rpmbuild_version ${FILEGDBAPI_VERSION}" \
        --define "rpmbuild_release ${FILEGDBAPI_RELEASE}" \
        -bb SPECS/FileGDBAPI.spec
fi

# GEOS
if [ ! -f $RPM_X86_64/$GEOS_RPM ]; then
    echo "#### Building RPM: GEOS"

    # Build image for building GEOS.
    docker build \
           --build-arg "packages=$( spec_requires geos )" \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-generic \
           -t hootenanny/rpmbuild-geos \
           $SCRIPT_HOME

    # Generate GEOS RPM.
    run_dep_image \
        -i hootenanny/rpmbuild-geos \
        rpmbuild \
        --define "rpmbuild_version ${GEOS_VERSION}" \
        --define "rpmbuild_release ${GEOS_RELEASE}" \
        -bb SPECS/geos.spec
fi

# glpk
if [ ! -f $RPM_X86_64/$GLPK_RPM ]; then
    echo "#### Building RPM: glpk"

    # Build image for glpk.
    docker build \
           --build-arg "packages=$( spec_requires glpk )" \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-generic \
           -t hoot/rpmbuild-glpk \
           $SCRIPT_HOME

    # Generate glpk RPM.
    run_dep_image \
        -i hoot/rpmbuild-glpk \
        rpmbuild -bb SPECS/glpk.spec
fi

# libgeotiff
if [ ! -f $RPM_X86_64/$LIBGEOTIFF_RPM ]; then
    echo "#### Building RPM: libgeotiff"

    # Build image for building libgeotiff.
    docker build \
           --build-arg "packages=$( spec_requires libgeotiff )" \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-generic \
           -t hootenanny/rpmbuild-libgeotiff \
           $SCRIPT_HOME

    # Generate libgeotiff RPM.
    run_dep_image \
        -i hootenanny/rpmbuild-libgeotiff \
        rpmbuild \
        --define "rpmbuild_version ${LIBGEOTIFF_VERSION}" \
        --define "rpmbuild_release ${LIBGEOTIFF_RELEASE}" \
        -bb SPECS/libgeotiff.spec
fi

# libkml
if [ ! -f $RPM_X86_64/$LIBKML_RPM ]; then
    echo "#### Building RPM: libkml"

    # Build image for building libkml.
    docker build \
           --build-arg "packages=$( spec_requires libkml )" \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-generic \
           -t hootenanny/rpmbuild-libkml \
           $SCRIPT_HOME

    # Generate libkml RPM.
    run_dep_image \
        -i hootenanny/rpmbuild-libkml \
        rpmbuild \
        --define "rpmbuild_version ${LIBKML_VERSION}" \
        --define "rpmbuild_release ${LIBKML_RELEASE}" \
        -bb SPECS/libkml.spec
fi

# NodeJS
if [ ! -f $RPM_X86_64/$NODEJS_RPM ]; then
    echo "#### Building RPM: NodeJS"

    # Build image for building NodeJS.
    docker build \
           --build-arg "packages=$( spec_requires nodejs )" \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-generic \
           -t hootenanny/rpmbuild-nodejs \
           $SCRIPT_HOME

    # Generate NodeJS RPM.
    run_dep_image \
        -i hootenanny/rpmbuild-nodejs \
        rpmbuild \
        --define "rpmbuild_version ${NODEJS_VERSION}" \
        --define "rpmbuild_release ${NODEJS_RELEASE}" \
        -bb SPECS/nodejs.spec
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
           -t hootenanny/rpmbuild-gdal \
           $SCRIPT_HOME

    # Generate GDAL RPM.
    run_dep_image \
        -i hootenanny/rpmbuild-gdal \
        rpmbuild \
        --define "rpmbuild_version ${GDAL_VERSION}" \
        --define "rpmbuild_release ${GDAL_RELEASE}" \
        -bb SPECS/hoot-gdal.spec
fi

# PostGIS
if [ ! -f $RPM_X86_64/$POSTGIS_RPM ]; then
    echo "#### Building RPM: PostGIS"

    docker build \
           --build-arg "packages=$( spec_requires hoot-postgis24 )" \
           --build-arg gdal_version=$GDAL_VERSION-$GDAL_RELEASE \
           -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-postgis \
           -t hootenanny/rpmbuild-postgis \
           $SCRIPT_HOME

    run_dep_image \
        -i hootenanny/rpmbuild-postgis \
        rpmbuild \
        --define "rpmbuild_version ${POSTGIS_VERSION}" \
        --define "rpmbuild_release ${POSTGIS_RELEASE}" \
        -bb SPECS/hoot-postgis24.spec
fi

## Simple Dependencies

# dumb-init
if [ ! -f $RPM_X86_64/$DUMBINIT_RPM ]; then
    echo "#### Building RPM: dumb-init"
    run_dep_image \
        rpmbuild \
        --define "rpmbuild_version ${DUMBINIT_VERSION}" \
        --define "rpmbuild_release ${DUMBINIT_RELEASE}" \
        -bb SPECS/dumb-init.spec
fi

# hoot-words
if [ ! -f $RPM_NOARCH/$WORDS_RPM ]; then
    echo "#### Building RPM: hoot-words"

    # Generate hoot-words RPM, but make SOURCES writable as the dictionary
    # file is a download and too big for version control.
    run_dep_image \
        -s rw \
        rpmbuild \
        --define "rpmbuild_version ${WORDS_VERSION}" \
        --define "rpmbuild_release ${WORDS_RELEASE}" \
        -bb SPECS/hoot-words.spec
fi

# osmosis
if [ ! -f $RPM_NOARCH/$OSMOSIS_RPM ]; then
    echo "#### Building RPM: osmosis"
    run_dep_image \
        rpmbuild \
        --define "rpmbuild_version ${OSMOSIS_VERSION}" \
        --define "rpmbuild_release ${OSMOSIS_RELEASE}" \
        -bb SPECS/osmosis.spec
fi

# stxxl
if [ ! -f $RPM_X86_64/$STXXL_RPM ]; then
    echo "#### Building RPM: stxxl"
    run_dep_image \
        rpmbuild \
        --define "rpmbuild_version ${STXXL_VERSION}" \
        --define "rpmbuild_release ${STXXL_RELEASE}" \
        -bb SPECS/stxxl.spec
fi

# su-exec
if [ ! -f $RPM_X86_64/$SUEXEC_RPM ]; then
    echo "#### Building RPM: su-exec"
    run_dep_image \
        rpmbuild \
        --define "rpmbuild_version ${SUEXEC_VERSION}" \
        --define "rpmbuild_release ${SUEXEC_RELEASE}" \
        -bb SPECS/su-exec.spec
fi

# tomcat8
if [ ! -f $RPM_NOARCH/$TOMCAT8_RPM ]; then
    echo "#### Building RPM: tomcat8"
    run_dep_image \
        rpmbuild \
        --define "rpmbuild_version ${TOMCAT8_VERSION}" \
        --define "rpmbuild_release ${TOMCAT8_RELEASE}" \
        -bb SPECS/tomcat8.spec
fi

# wamerican-insane
if [ ! -f $RPM_NOARCH/$WAMERICAN_RPM ]; then
    echo "#### Building RPM: wamerican-insane"
    run_dep_image \
        rpmbuild \
        --define "rpmbuild_version ${WAMERICAN_VERSION}" \
        --define "rpmbuild_release ${WAMERICAN_RELEASE}" \
        -bb SPECS/wamerican-insane.spec
fi
