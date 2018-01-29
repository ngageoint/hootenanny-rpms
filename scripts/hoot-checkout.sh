#!/bin/bash
set -euo pipefail
GIT_COMMIT="${1:-develop}"
HOOT_DEST=${HOOT_DEST:-$HOME/hootenanny}
HOOT_REPO=${HOOT_REPO:-https://github.com/ngageoint/hootenanny.git}

if [ ! -d $HOOT_DEST/.git ]; then
    git clone $HOOT_REPO $HOOT_DEST
fi

pushd $HOOT_DEST
git clean -q -f -d -x
git pull
git checkout $GIT_COMMIT
git submodule update --init --recursive
popd
