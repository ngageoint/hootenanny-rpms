#!/bin/bash
set -euo pipefail

# Default variables.
DEST=$(pwd)
BUCKET=hoot-rpm
KEEP=5
PREFIX=develop
USAGE=no

# These variables default to value of AWS CLI environment
# variables (if defined).
set +u
PROFILE=${AWS_PROFILE:-hoot-rpm-develop}
REGION=${AWS_DEFAULT_REGION:-us-east-1}
set -u

while getopts ":a:b:d:k:p:r:" opt; do
    case "${opt}" in
        a)
            PROFILE="${OPTARG}"
            ;;
        b)
            BUCKET="${OPTARG}"
            ;;
        d)
            DEST="${OPTARG}"
            ;;
        k)
            KEEP="${OPTARG}"
            ;;
        p)
            PREFIX="${OPTARG}"
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

# Abort if invalid options.
if [ "${USAGE}" == "yes" ]; then
    echo "repo_sync.sh: [-a <AWS Profile>] [-b <S3 Bucket>] [-d <Local Destination>] [-p <S3 Prefix>] [-r <AWS Region>]"
    exit 1
fi


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
REPO_TS=$(aws s3api head-object --bucket $BUCKET --key $PREFIX/repodata/repomd.xml --query LastModified --profile $PROFILE --region $REGION --output text 2>/dev/null || printf none)

if [ "${REPO_TS}" == "none" ]; then
    # Initialize the yum repository, as it doesn't exist in S3.
    createrepo --database --unique-md-filenames --deltas $REPO

    # Ensure a hoot.repo exists for use with yum-config-manager.
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
else
    # The repo already exists, sync the repository data, but keep
    # any newer files/rpms.
    aws s3 sync $S3_URL $REPO --profile $PROFILE --region $REGION --keep-newer
fi

# Only keep as many packages as specified.
repomanage --keep $KEEP --old $REPO | xargs rm -f -v

# Update the repository metadata.
createrepo --update $REPO

# Sync back to the mothership, deleting
aws s3 sync $REPO $S3_URL --delete --profile $PROFILE --region $REGION
