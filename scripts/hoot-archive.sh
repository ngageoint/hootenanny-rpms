#!/bin/bash
set -euo pipefail
HOOT_REPO="${HOOT_REPO:-${HOME}/hootenanny}"

if [ ! -d "$HOOT_REPO/.git" ]; then
    echo 'Please checkout Hootenanny repository first.'
    exit 1
fi

ARCHIVE_SCRIPT="$HOOT_REPO/scripts/ci/archive.sh"
if [ -x "$ARCHIVE_SCRIPT" ]; then
    $ARCHIVE_SCRIPT
else
    # This revision of Hootenanny doesn't have the archive script, so generate
    # one manually.
    pushd "$HOOT_REPO"
    cp LocalConfig.pri.orig LocalConfig.pri

    # Temporarily allow undefined variables to allow us to source `SetupEnv.sh`.
    set +u
    source SetupEnv.sh
    set -u

    source conf/database/DatabaseConfig.sh

    # Generate configure script.
    aclocal
    autoconf
    autoheader
    automake --add-missing --copy

    # Run configure, enable R&D, services, and PostgreSQL.
    ./configure --quiet --with-rnd --with-services --with-postgresql

    # Make the archive.
    make -j"$(nproc)" clean
    make -j"$(nproc)" archive
    popd
fi
