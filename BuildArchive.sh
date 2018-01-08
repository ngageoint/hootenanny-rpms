#!/bin/bash
set -euo pipefail

## Get variables.
SCRIPT_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $SCRIPT_HOME/Vars.sh

# The container used to build Hootenanny archive.
BUILD_IMAGE="${BUILD_IMAGE:-hoot/rpmbuild-hoot-release}"

mkdir -p $SCRIPT_HOME/hootenanny $SCRIPT_HOME/m2

docker run \
       -v $SOURCES:/rpmbuild/SOURCES:rw \
       -v $SPECS:/rpmbuild/SPECS:ro \
       -v $RPMS:/rpmbuild/RPMS:rw \
       -v $SCRIPT_HOME/scripts:/rpmbuild/scripts:ro \
       -v $SCRIPT_HOME/hootenanny:/rpmbuild/hootenanny:rw \
       -v $SCRIPT_HOME/m2:/rpmbuild/.m2:rw \
       -it --rm \
       $BUILD_IMAGE \
       /bin/bash -c '/rpmbuild/scripts/hoot-checkout.sh && /rpmbuild/scripts/hoot-archive.sh'
