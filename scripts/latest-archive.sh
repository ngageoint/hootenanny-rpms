#!/bin/bash
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
