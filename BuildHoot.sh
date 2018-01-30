#!/bin/bash
set -euo pipefail

## Get variables.
SCRIPT_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $SCRIPT_HOME/Vars.sh

BUILD_IMAGE=${BUILD_IMAGE:-hoot/rpmbuild-hoot-release}

set +u
if [ -z $1 ]; then
    HOOT_ARCHIVE_VERSION=$( latest_hoot_archive_version )
else
    HOOT_ARCHIVE_VERSION=$1
fi
set -u

# Set RPM macros for versions that are used in the container.
run_hoot_image \
    -i $BUILD_IMAGE \
    rpmbuild \
      --define "%gdal_version %(gdal-config --version)" \
      --define "%hoot_version ${HOOT_ARCHIVE_VERSION}" \
      --define "%nodejs_version %(rpm -q --queryformat '%%{version}' nodejs)" \
      --define "%stxxl_version %(rpm -q --queryformat '%%{version}' stxxl)" \
      --define "%tomcat_version %(rpm -q --queryformat '%%{version}' tomcat8)" \
      -bb SPECS/hootenanny.spec
