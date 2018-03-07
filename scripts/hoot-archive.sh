#!/bin/bash
set -euo pipefail
HOOT_REPO="${HOOT_REPO:-${HOME}/hootenanny}"

if [ ! -d $HOOT_REPO/.git ]; then
    echo 'Please checkout Hootenanny repository first.'
    exit 1
fi

pushd $HOOT_REPO
cp LocalConfig.pri.orig LocalConfig.pri

# TODO: Do we add `ccache` like in original `BuildArchive.sh`?
#echo "QMAKE_CXX=ccache g++" >> LocalConfig.pri

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

# Update the license headers.
./scripts/copyright/UpdateAllCopyrightHeaders.sh

# Make the archive.
make -j$(nproc) clean
make -j$(nproc) archive

# Copy in source archive to RPM sources.
cp -v hootenanny-[0-9]*.tar.gz $HOME/SOURCES
popd
