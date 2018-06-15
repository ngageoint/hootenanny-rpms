#!/bin/bash
set -euo pipefail

# Defaults.
USAGE=no
ARCHIVE=""
BUCKET=""
PREFIX=""

while getopts ":a:b:p:" opt; do
    case "$opt" in
        a)
            ARCHIVE="$OPTARG"
            ;;
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
    echo "query-archive.sh: -a <Archive Name> -b <S3 Bucket> -p <Bucket Prefix>"
    exit 1
}

# Abort if invalid options.
if [[ "$USAGE" = "yes" || -z "$ARCHIVE" || -z "$BUCKET" || -z "$PREFIX" ]]; then
    usage
fi

# Pull out the git commit from the archive filename.
GIT_COMMIT="$(basename "$ARCHIVE" | awk -F_ "{ git_abbrev = \$3; sub(/.tar.gz/, \"\", git_abbrev); print substr(git_abbrev, 2) }")"

# Query the number of RPMs
aws s3api list-objects-v2 \
    --bucket "$BUCKET" \
    --prefix "$PREFIX" \
    --query "length(Contents[?ends_with(Key, \`$GIT_COMMIT.el7.x86_64.rpm\`) && starts_with(Key, \`$PREFIX/hootenanny-core-\`)].Key)"
