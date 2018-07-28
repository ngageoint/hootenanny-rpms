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

# Default variables.
HOOT_BRANCH="${HOOT_BRANCH:-develop}"
ARCHIVE_BUCKET="${ARCHIVE_BUCKET:-hoot-archives}"
ARCHIVE_PREFIX="${ARCHIVE_PREFIX:-circle/$HOOT_BRANCH}"
REPO_BUCKET="${REPO_BUCKET:-hoot-repo}"
REPO_PREFIX="${REPO_PREFIX:-el7/$HOOT_BRANCH}"

# Ensure directory structure in place for using the shell scripts
mkdir -p cache/m2 cache/npm el7 RPMS

# Determine what the latest development archive is.
LATEST_ARCHIVE="$(./scripts/latest-archive.sh -b "$ARCHIVE_BUCKET" -p "$ARCHIVE_PREFIX")"

# Query the development repository for number of RPMs with the
# archive's git hash.
NUM_RPMS="$(./scripts/query-archive.sh -a "$LATEST_ARCHIVE" -b "$REPO_BUCKET" -p "$REPO_PREFIX")"

if [ "$NUM_RPMS" = "0" ]; then
    # Retrieve the latest archive.
    aws s3 cp "s3://$ARCHIVE_BUCKET/$LATEST_ARCHIVE" SOURCES/ --quiet

    # Seed the Maven cache.
    source shell/Vars.sh
    maven_cache

    # Change ownership permissions on directories accessed in container to
    # match that of the rpmbuild user in the public Docker Hub.
    sudo chown -R 1000:1000 cache el7 RPMS SOURCES

    # Build the RPM and copy RPMs into workspace folder.
    ./shell/BuildHoot.sh
    sudo mv -v RPMS/{noarch,x86_64}/*.rpm el7
else
    touch el7/none.rpm
fi
