#!/bin/bash
# Copyright (C) 2018-2021 Maxar Technologies (https://www.maxar.com)
#
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
source "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/Vars.sh

# Build base images.
build_base_images

# The "release" image, built with latest signed dependencies in the hootenanny
# public repository.
docker build \
       --build-arg "packages=$( spec_requires hootenanny )" \
       --build-arg mocha_version=$MOCHA_VERSION \
       --build-arg nodejs_version=$NODEJS_VERSION-$NODEJS_RELEASE \
       --build-arg pg_version=$PG_VERSION \
       -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-hoot-release \
       -t hootenanny/rpmbuild-hoot-release \
       $SCRIPT_HOME
