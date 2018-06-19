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
            if [ "${PREFIX: -1}" = "/" ]; then
                echo "Prefix cannot end with a '/'."
                exit 2
            fi
            ;;
        *)
            USAGE=yes
            ;;
    esac
done
shift $((OPTIND-1))


function usage() {
    echo "query-archive.sh: -a <Archive Name> -b <S3 Bucket> -p <Bucket Prefix>"
    echo "  Queries the yum repository for an RPM built from the archive"
    echo "  hosted at the given S3 bucket and prefix.  Prints the number"
    echo "  of RPMs found or '0' if none exist."
    exit 1
}

# Abort if invalid options.
if [[ "$USAGE" = "yes" || -z "$ARCHIVE" || -z "$BUCKET" || -z "$PREFIX" ]]; then
    usage
fi

# Pull out the git commit from the archive filename.
GIT_COMMIT="$(basename "$ARCHIVE" | awk -F_ "{ git_abbrev = \$3; sub(/.tar.gz/, \"\", git_abbrev); print substr(git_abbrev, 2) }")"

# Query the number of RPMs; have to append a "/" to prefix, otherwise AWS
# won't allow the query expression.
aws s3api list-objects-v2 \
    --bucket "$BUCKET" \
    --prefix "$PREFIX/" \
    --query "length(Contents[?ends_with(Key, \`$GIT_COMMIT.el7.x86_64.rpm\`) && starts_with(Key, \`$PREFIX/hootenanny-core-\`)].Key)"
