#!/bin/bash
set -euo pipefail
GIT_COMMIT="${GIT_COMMIT:-develop}"
HOOT_REPO="${HOOT_REPO:-${HOME}/hootenanny}"

if [ ! -d $HOOT_REPO/.git ]; then
    git clone https://github.com/ngageoint/hootenanny.git $HOOT_REPO
fi

pushd $HOOT_REPO
git clean -q -f -d -x
git pull
git checkout $GIT_COMMIT
git submodule update --init --recursive
popd
