#!/bin/bash

HOOT_RPM_PREFIX="hootenanny-autostart"
PREVIOUS_VERSION="$(sudo yum list --showduplicates hootenanny-autostart | \
                      tail -n 2 | \
                      head -1 | \
                      awk '{ print $2 }')"

# if the previous version couldn't be discovered in the hoot yum repo
# then print an error message and exit 
if [ -z "$PREVIOUS_VERSION" ]; then
    echo "Failed to discover the previous RPM version of Hootenanny"
    exit 1
fi

INSTALLED_HOOT_VERSION="$(rpm -qa | grep $HOOT_RPM_PREFIX)"
# if a version of hoot is already install downgrade it
# else install the 2nd latest version of hootenanny
if [ ! -z "$INSTALLED_HOOT_VERSION" ]; then
    sudo yum -y downgrade "${HOOT_RPM_PREFIX}-${PREVIOUS_VERSION}"
else
    sudo yum -y install "${HOOT_RPM_PREFIX}-${PREVIOUS_VERSION}"
fi
