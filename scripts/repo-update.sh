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

set +u
if [ -z "$1" ]; then
    echo 'repo-update.sh: must provide a repository directory argument.'
    exit 1
fi
set -u

REPO="$1"
REPODATA="$REPO/repodata"

if [ ! -d "$REPO" ] ; then
    mkdir -p "$REPO"
fi

# Update (or create) the repository database with `createrepo`.
if [ ! -d "$REPODATA" ]; then
    createrepo --database --unique-md-filenames --deltas "$REPO"
else
    createrepo --update "$REPO"
fi
