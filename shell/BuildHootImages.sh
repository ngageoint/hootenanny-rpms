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
BUILD_IMAGE="${1:-release}"
set -u

## Get variables.
source "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/Vars.sh

# Build base images.
build_base_images

case "${BUILD_IMAGE}" in
    # The development image is built entirely using local RPMs, built
    # with the `BuildDeps.sh` script.
    devel)
        docker build \
               --build-arg "packages=$( spec_requires hootenanny )" \
               --build-arg dumbinit_version=$DUMBINIT_VERSION-$DUMBINIT_RELEASE \
               --build-arg glpk_version=$GLPK_VERSION-$GLPK_RELEASE \
               --build-arg libphonenumber_version="$LIBPHONENUMBER_VERSION-$LIBPHONENUMBER_RELEASE" \
               --build-arg liboauthcpp_version="$LIBOAUTHCPP_VERSION-$LIBOAUTHCPP_RELEASE" \
               --build-arg libpostal_version="$LIBPOSTAL_VERSION-$LIBPOSTAL_RELEASE" \
               --build-arg mocha_version=$MOCHA_VERSION \
               --build-arg pg_version=$PG_VERSION \
               --build-arg nodejs_version=$NODEJS_VERSION-$NODEJS_RELEASE \
               --build-arg npm_version=$NPM_VERSION-$NPM_RELEASE.$NODEJS_VERSION.$NODEJS_RELEASE \
               --build-arg osmosis_version=$OSMOSIS_VERSION-$OSMOSIS_RELEASE \
               --build-arg stxxl_version=$STXXL_VERSION-$STXXL_RELEASE \
               --build-arg suexec_version=$SUEXEC_VERSION-$SUEXEC_RELEASE \
               --build-arg tomcat8_version=$TOMCAT8_VERSION-$TOMCAT8_RELEASE \
               --build-arg v8_version=$V8_VERSION-$V8_RELEASE.$NODEJS_VERSION.$NODEJS_RELEASE \
               --build-arg words_version=$WORDS_VERSION-$WORDS_RELEASE \
               -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-hoot-devel \
               -t hootenanny/rpmbuild-hoot-devel \
               $SCRIPT_HOME
        ;;
    # The "release" image, built with latest signed dependencies in the hootenanny
    # public repository.
    release)
        docker build \
               --build-arg "packages=$( spec_requires hootenanny )" \
               --build-arg mocha_version=$MOCHA_VERSION \
               --build-arg nodejs_version=$NODEJS_VERSION-$NODEJS_RELEASE \
               --build-arg pg_version=$PG_VERSION \
               -f $SCRIPT_HOME/docker/Dockerfile.rpmbuild-hoot-release \
               -t hootenanny/rpmbuild-hoot-release \
               $SCRIPT_HOME
        ;;
    *)
        echo 'Invalid build image.'
        exit 1
        ;;
esac
