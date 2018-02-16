#!/bin/bash
set -euo pipefail

set +u
if [ -z $1 ]; then
    echo 'repo-sign.sh: must provide a repository directory argument.'
    exit 1
fi
set -u

REPO=$1
REPODATA=$REPO/repodata
REPOMD=$REPODATA/repomd.xml

# Sign the repository metadata file.
gpg --detach-sign --armor $REPOMD
