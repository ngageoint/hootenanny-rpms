#!/bin/bash
set -euo pipefail

DEST=$(pwd)
BUCKET=hoot-rpm
PREFIX=develop

set +u
REGION=${AWS_DEFAULT_REGION:-us-east-1}
set -u

while getopts ":b:d:p:r:" opt; do
    case "${opt}" in
        b)
            BUCKET="${OPTARG}"
            ;;
        d)
            DEST="${OPTARG}"
            ;;
        p)
            PREFIX="${OPTARG}"
            ;;
        r)
            REGION="${OPTARG}"
            ;;
        *)
            usage=yes
            ;;
    esac
done
shift $((OPTIND-1))

## Setting up.
REPO=$DEST/$PREFIX

S3_URL="s3://${BUCKET}/${PREFIX}"
if [ "${REGION}" == "us-east-1" ]; then
    S3_HOST=s3.amazonaws.com
else
    S3_HOST=s3-$REGION.amazonaws.com
fi

if [ ! -d $REPO ] ; then
    mkdir -p $REPO
fi

# If the repo exists, grab it's last modified timestamp.
REPO_TS=$(aws s3api head-object --bucket hoot-rpm --key $PREFIX/repodata/repomd.xml --query LastModified --region $REGION --output text 2>/dev/null || printf none)

if [ "${REPO_TS}" == "none" ]; then
    createrepo --database --unique-md-filenames --deltas $REPO
else
    mkdir -p $REPO/repodata

    # The repo already exists, sync the repository data.
    aws s3 sync $S3_URL/repodata $REPO/repodata --region $REGION

    # TODO: Go through existing RPMs
fi

# Bail early before untested code.
exit 0

# Ensure a hoot.repo exists for use with yum-config-manager.
if [ ! -d $REPO/hoot.repo]; then
    echo "cat > $REPO/hoot.repo <<EOF"
     cat > $REPO/hoot.repo <<EOF
[hoot-develop]
name = Hootenanny Development
baseurl = https://${S3_HOST}/${BUCKET}/${PREFIX}
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


# Prune old packages.
aws s3 sync $REPO/ $S3_URL --delete --region $REGION
