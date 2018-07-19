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
source "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/Vars.sh

BUILD_IMAGE=${BUILD_IMAGE:-hootenanny/rpmbuild-hoot-release}

set +u
if [ -z $1 ]; then
    HOOT_VERSION_GEN=$( latest_hoot_version_gen )
else
    HOOT_VERSION_GEN=$1
fi
set -u

# Set RPM macros for versions that are used in the container.
run_hoot_build_image \
    -i $BUILD_IMAGE \
    rpmbuild \
      --define "hoot_version_gen ${HOOT_VERSION_GEN}" \
      --define "geos_version %(rpm -q --queryformat '%%{version}' geos)" \
      --define "glpk_version %(rpm -q --queryformat '%%{version}' glpk)" \
      --define "gdal_version %(rpm -q --queryformat '%%{version}' hoot-gdal)" \
      --define "nodejs_version %(rpm -q --queryformat '%%{version}' nodejs)" \
      --define "stxxl_version %(rpm -q --queryformat '%%{version}' stxxl)" \
      --define "tomcat_version %(rpm -q --queryformat '%%{version}' tomcat8)" \
      -bb SPECS/hootenanny.spec
