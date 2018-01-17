#!/bin/bash
set -euo pipefail

## Get variables.
SCRIPT_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $SCRIPT_HOME/Vars.sh

# The container used to build Hootenanny archive.
BUILD_IMAGE=${BUILD_IMAGE:-hoot/rpmbuild-hoot-release}

run_hoot_image \
    -i $BUILD_IMAGE -s rw \
    /bin/bash -c '/rpmbuild/scripts/hoot-checkout.sh && /rpmbuild/scripts/hoot-archive.sh'
