#!/bin/bash
set -euo pipefail

## Get variables.
SCRIPT_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $SCRIPT_HOME/Vars.sh

BUILD_IMAGE=${BUILD_IMAGE:-hoot/rpmbuild-hoot-release}
HOOT_ARCHIVE=${HOOT_ARCHIVE:-$(ls -1t $SOURCES/hootenanny-[0-9]*.tar.gz | head -n1)}
HOOT_VERSION=${HOOT_ARCHIVE##$SOURCES/hootenanny-}
HOOT_VERSION=${HOOT_VERSION%%.tar.gz}

run_hoot_image \
    -i $BUILD_IMAGE \
    rpmbuild \
      --define "%hoot_version ${HOOT_VERSION}" \
      -bb SPECS/hootenanny.spec
