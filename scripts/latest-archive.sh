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

# Defaults.
USAGE=no
BUCKET=""
PREFIX=""

while getopts ":b:p:" opt; do
    case "$opt" in
        b)
            BUCKET="$OPTARG"
            ;;
        p)
            PREFIX="$OPTARG"
            ;;
        *)
            USAGE=yes
            ;;
    esac
done
shift $((OPTIND-1))


function usage() {
    echo "latest-archive.sh: -b <S3 Bucket> -p <Bucket Prefix>"
    echo "  Prints the latest archive file hosted at the given S3 bucket and prefix."
    exit 1
}

# Abort if invalid options.
if [[ "$USAGE" = "yes" || -z "$BUCKET" || -z "$PREFIX" ]]; then
    usage
fi

# Use a query expression to determine the number of objects in the
# bucket that match the prefix.
NUM_ARCHIVES="$(aws s3api list-objects-v2 --bucket "$BUCKET" --prefix "$PREFIX" --query "type(Contents[]) == \`array\` && length(Contents[]) || \`0\`")"

if [ "$NUM_ARCHIVES" = "0" ]; then
    # Bail if no archives are found.
    echo "No archives found in s3://$BUCKET/$PREFIX"
    exit 2
else
    # Otherwise, just print out the key of the latest archive.  This is done
    # with reverse sorting on the last modified date for every object in the
    # query expression.
    aws s3api list-objects-v2 \
        --bucket "$BUCKET" \
        --prefix "$PREFIX" \
        --output text \
        --query 'reverse(sort_by(Contents[].{LastModified: LastModified, Key: Key}, &LastModified))[0].Key'
fi
