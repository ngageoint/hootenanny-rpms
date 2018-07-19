#!/bin/bash
# Copyright (C) 2018 Radiant Solutions (http://www.radiantsolutions.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
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

mv -v "$HOOT_REPO"/hootenanny-[0-9]*.tar.gz "$HOME/SOURCES"
