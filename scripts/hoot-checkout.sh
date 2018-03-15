#!/bin/bash
set -euo pipefail
GIT_COMMIT="${1:-develop}"
HOOT_DEST=${HOOT_DEST:-$HOME/hootenanny}
HOOT_REPO=${HOOT_REPO:-https://github.com/ngageoint/hootenanny.git}

if [ ! -d $HOOT_DEST/.git ]; then
    git clone $HOOT_REPO $HOOT_DEST
fi

pushd $HOOT_DEST
# Clean out any untracked files.
git clean -q -f -d -x

# Update tags.
git fetch --tags

# Checkout desired commit; pull latest when on a branch.
git checkout $GIT_COMMIT
if git symbolic-ref --short HEAD; then
    git pull
fi

# Update submodules.
git submodule update --init --recursive
popd
