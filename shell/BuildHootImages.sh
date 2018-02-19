#!/bin/bash
set -euo pipefail

set +u
BUILD_IMAGE="${1:-release}"
set -u

## Get variables.
source "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/Vars.sh

# Build base images.
build_base_images

case "${BUILD_IMAGE}" in
    # The development image is built entirely using local RPMs, built
    # with the `BuildDeps.sh` script.
    devel)
        docker build \
               --build-arg "packages=$( spec_requires hootenanny )" \
               --build-arg dumbinit_version=$DUMBINIT_VERSION-$DUMBINIT_RELEASE \
               --build-arg filegdbapi_version=$FILEGDBAPI_VERSION-$FILEGDBAPI_RELEASE \
               --build-arg gdal_version=$GDAL_VERSION-$GDAL_RELEASE \
               --build-arg geos_version=$GEOS_VERSION-$GEOS_RELEASE \
               --build-arg libgeotiff_version=$LIBGEOTIFF_VERSION-$LIBGEOTIFF_RELEASE \
               --build-arg libkml_version=$LIBKML_VERSION-$LIBKML_RELEASE \
               --build-arg mocha_version=$MOCHA_VERSION \
               --build-arg pg_version=$PG_VERSION \
               --build-arg postgis_version=$POSTGIS_VERSION-$POSTGIS_RELEASE \
               --build-arg nodejs_version=$NODEJS_VERSION-$NODEJS_RELEASE \
               --build-arg osmosis_version=$OSMOSIS_VERSION-$OSMOSIS_RELEASE \
               --build-arg stxxl_version=$STXXL_VERSION-$STXXL_RELEASE \
               --build-arg suexec_version=$SUEXEC_VERSION-$SUEXEC_RELEASE \
               --build-arg tomcat8_version=$TOMCAT8_VERSION-$TOMCAT8_RELEASE \
               --build-arg words_version=$WORDS_VERSION-$WORDS_RELEASE \
               -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-hoot-devel \
               -t hootenanny/rpmbuild-hoot-devel \
               $SCRIPT_HOME
        ;;
    # The "release" image, built with latest signed images in the hootenanny
    # public repository.
    release)
        docker build \
               --build-arg "packages=$( spec_requires hootenanny )" \
               --build-arg mocha_version=$MOCHA_VERSION \
               --build-arg nodejs_version=$NODEJS_VERSION-$NODEJS_RELEASE \
               --build-arg pg_version=$PG_VERSION \
               -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-hoot-release \
               -t hootenanny/rpmbuild-hoot-release \
               $SCRIPT_HOME
        ;;
    *)
        echo 'Invalid build image.'
        exit 1
        ;;
esac
