#!/bin/bash
set -euo pipefail

## Get variables.
source "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/Vars.sh

BUILD_IMAGE=${BUILD_IMAGE:-hootenanny/rpmbuild-hoot-release}

set +u
if [ -z $1 ]; then
    HOOT_VERSION_GEN=$( latest_hoot_version_gen )
else
    HOOT_VERSION_GEN=$1
fi
set -u

# Set RPM macros for versions that are used in the container.
run_hoot_build_image \
    -i $BUILD_IMAGE \
    rpmbuild \
      --define "gdal_version %(gdal-config --version)" \
      --define "hoot_version_gen ${HOOT_VERSION_GEN}" \
      --define "nodejs_version %(rpm -q --queryformat '%%{version}' nodejs)" \
      --define "stxxl_version %(rpm -q --queryformat '%%{version}' stxxl)" \
      --define "tomcat_version %(rpm -q --queryformat '%%{version}' tomcat8)" \
      -bb SPECS/hootenanny.spec