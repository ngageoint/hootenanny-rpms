#!/bin/bash
set -euo pipefail

GPG_PATH=${GPG_PATH:-$HOME/.gnupg-hoot}
REPO=${REPO:-$SCRIPT_HOME/el7}

if [ ! -d $REPO ] ; then
    mkdir -p $REPO
fi

docker run \
  -v $GPG_PATH:/rpmbuild/.gnupg:rw \     
  -v $RPMS:/rpmbuild/RPMS:ro \
  -it --rm \
  hoot/rpmbuild-repo \
           rpmbuild -bb SPECS/wamerican-insane.spec
