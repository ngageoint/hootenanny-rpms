#!/bin/bash

set -euo pipefail

PGDG_REPO="${PGDG_REPO:-https://s3.amazonaws.com/hoot-repo/el7/pgdg95.repo}"
HOOT_REPO="${HOOT_REPO:-https://s3.amazonaws.com/hoot-repo/el7/develop/hoot.repo}"

sudo yum install -y epel-release yum-utils
sudo yum-config-manager --add-repo "$PGDG_REPO"
sudo yum-config-manager --add-repo "$HOOT_REPO"
sudo yum makecache -y