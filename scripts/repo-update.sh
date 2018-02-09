#!/bin/bash
set -euo pipefail

set +u
if [ -z $1 ]; then
    echo 'repo-update.sh: must provide a repository directory argument.'
    exit 1
fi
set -u

REPO=$1
REPODATA=$REPO/repodata
REPOMD=$REPODATA/repomd.xml

if [ ! -d $REPO ] ; then
    mkdir -p $REPO
fi

# Update (or create) the repository database with `createrepo`.
if [ ! -d $REPODATA ]; then
    createrepo --database --unique-md-filenames --deltas $REPO
else
    createrepo --update $REPO
fi
