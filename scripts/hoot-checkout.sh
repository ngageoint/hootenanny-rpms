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
GIT_COMMIT="${1:-develop}"
HOOT_DEST="${HOOT_DEST:-$HOME/hootenanny}"
HOOT_REPO="${HOOT_REPO:-https://github.com/ngageoint/hootenanny.git}"

if [ ! -d "$HOOT_DEST/.git" ]; then
    git clone "$HOOT_REPO" "$HOOT_DEST"
fi

pushd "$HOOT_DEST"
# Clean out any untracked files.
git clean -q -f -d -x

# Update tags.
git fetch --tags

# Checkout desired commit; pull latest when on a branch.
git checkout "$GIT_COMMIT"
if git symbolic-ref --short HEAD; then
    git pull
fi

# Update submodules.
git submodule update --init --recursive
popd
