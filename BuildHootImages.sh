#!/bin/bash
set -e

## Get variables.
SCRIPT_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $SCRIPT_HOME/Vars.sh

# Build base images.
build_base_images

# Get RPM build requirements.
HOOT_REQUIRES=$( spec_requires hootenanny )

docker build \
  --build-arg "packages=${HOOT_REQUIRES}" \
  --build-arg node_version=$NODE_VERSION \
  --build-arg pg_version=$PG_VERSION \
  -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-hoot-release \
  -t hoot/rpmbuild-hoot-release \
  $SCRIPT_HOME

docker build \
  --build-arg "packages=${HOOT_REQUIRES}" \
  --build-arg filegdbapi_version=$FILEGDBAPI_VERSION-$FILEGDBAPI_RELEASE \
  --build-arg gdal_version=$GDAL_VERSION-$GDAL_RELEASE \
  --build-arg geos_version=$GEOS_VERSION-$GEOS_RELEASE \
  --build-arg libgeotiff_version=$LIBGEOTIFF_VERSION-$LIBGEOTIFF_RELEASE \
  --build-arg libkml_version=$LIBKML_VERSION-$LIBKML_RELEASE \
  --build-arg pg_version=$PG_VERSION \
  --build-arg postgis_version=$POSTGIS_VERSION-$POSTGIS_RELEASE \
  --build-arg node_version=$NODE_VERSION \
  --build-arg suexec_version=$SUEXEC_VERSION-$SUEXEC_RELEASE \
  -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-hoot-devel \
  -t hoot/rpmbuild-hoot-devel \
  $SCRIPT_HOME
