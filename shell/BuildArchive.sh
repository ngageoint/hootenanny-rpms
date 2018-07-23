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

## Get variables.
set +u
GIT_COMMIT="${1:-develop}"
set -u
source "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/Vars.sh

# The container used to build Hootenanny archive.
BUILD_IMAGE=${BUILD_IMAGE:-hootenanny/rpmbuild-hoot-release}

run_hoot_build_image \
    -i $BUILD_IMAGE -s rw \
    /bin/bash -c "/rpmbuild/scripts/hoot-checkout.sh ${GIT_COMMIT} && /rpmbuild/scripts/hoot-archive.sh"
