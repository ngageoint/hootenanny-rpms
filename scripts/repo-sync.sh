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
DEST="$(pwd)"
BUCKET=""
KEEP="10"
PREFIX=""
QUIET=""
UPLOAD="yes"
USAGE="no"

# These variables default to value of AWS CLI environment
# variables (if defined).
PROFILE="${AWS_PROFILE:-}"
REGION="${AWS_DEFAULT_REGION:-us-east-1}"

# Getting parameters from the command line.
while getopts ":a:b:p:d:k:nqr:" opt; do
    case "${opt}" in
        # Required parameters.
        b)
            BUCKET="${OPTARG}"
            ;;
        p)
            PREFIX="${OPTARG}"
            ;;
        # Optional parameters.
        a)
            PROFILE="${OPTARG}"
            ;;
        d)
            DEST="${OPTARG}"
            ;;
        k)
            KEEP="${OPTARG}"
            ;;
        n)
            UPLOAD="no"
            ;;
        q)
            QUIET="--quiet"
            ;;
        r)
            REGION="${OPTARG}"
            ;;
        *)
            USAGE=yes
            ;;
    esac
done
shift $((OPTIND-1))

# Setting up.
function usage() {
    echo "repo_sync.sh: -b <S3 Bucket> -p <S3 Prefix> [-a <AWS CLI Profile>] [-d <Local Destination>] [-k <Keep>] [-n No Upload] [-r <AWS Region>]"
    exit 1
}

# Abort if invalid options.
if [[ "${USAGE}" == "yes" || -z "${BUCKET}" || -z "${PREFIX}" ]]; then
    usage
fi

REPO="$DEST/$PREFIX"
S3_URL="s3://$BUCKET/$PREFIX"
if [ "$REGION" == "us-east-1" ]; then
    S3_HOST=s3.amazonaws.com
else
    S3_HOST=s3-$REGION.amazonaws.com
fi

# Setting up array of AWS common options.
AWS_COMMON_OPTS=(
    "--region=$REGION"
)
if [ -n "$PROFILE" ]; then
    AWS_COMMON_OPTS=(
        "${AWS_COMMON_OPTS[@]}"
        "--profile=$PROFILE"
    )
fi

if [ ! -d "$REPO" ] ; then
    mkdir -p "$REPO"
fi

# If the repo exists, grab it's last modified timestamp.
HEAD_OBJECT_OPTS=(
    "--bucket=$BUCKET"
    "--key=$PREFIX/repodata/repomd.xml"
    "--query=LastModified"
    "--output=text"
    "${AWS_COMMON_OPTS[@]}"
)

# If a repository already exists, it'll have a repository XML file
# in a known location.
REPO_TS="$(aws s3api head-object "${HEAD_OBJECT_OPTS[@]}" 2>/dev/null || printf none)"

if [ "$REPO_TS" = "none" ]; then
    # Initialize the yum repository, as it doesn't exist in S3.
    if [ ! -f "$REPO/repodata/repomd.xml" ] ; then
        createrepo --database --unique-md-filenames --deltas "$REPO"
    fi

    # Ensure a hoot.repo exists for use with yum-config-manager.
    if [ ! -f "$REPO/hoot.repo" ]; then
        cat > "$REPO/hoot.repo" <<EOF
[hoot-develop]
name = Hootenanny Development
baseurl = https://$S3_HOST/$BUCKET/$PREFIX
enabled = 1
gpgcheck = 0

[hoot-deps]
name = Hootenanny Dependencies
baseurl = https://s3.amazonaws.com/hoot-repo/el7/deps/release
enabled = 1
gpgcheck = 1
repo_gpgcheck = 1
gpgkey = https://s3.amazonaws.com/hoot-repo/el7/hoot.gpg
EOF
    fi
else
    # The repo already exists, sync the repository files down, but
    # keep local files that are more recent than what's in S3.
    DOWNLOAD_OPTS=(
        "$S3_URL"
        "$REPO"
        "--keep-newer"
        "$QUIET"
        "${AWS_COMMON_OPTS[@]}"
    )
    aws s3 sync "${DOWNLOAD_OPTS[@]}"
fi

# Only keep as many packages as specified, deleting older versions.
repomanage --keep "$KEEP" --old "$REPO" | xargs rm -f -v

# Update the repository metadata.
createrepo --update "$REPO"

if [ "$UPLOAD" == "yes" ]; then
    # Upload back to the S3 bucket, deleting any files not present locally.
    UPLOAD_OPTS=(
        "$REPO"
        "$S3_URL"
        "--delete"
        "$QUIET"
        "${AWS_COMMON_OPTS[@]}"
    )
    aws s3 sync "${UPLOAD_OPTS[@]}"
fi
