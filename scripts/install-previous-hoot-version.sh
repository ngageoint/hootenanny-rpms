#!/bin/bash

HOOT_RPM_PREFIX="hootenanny-autostart"
PREVIOUS_VERSION=`sudo yum list --showduplicates hootenanny-autostart | \
                      tail -n 2 |  \
                      head -1 | \
                      awk '{ print $2 }'`

INSTALLED_HOOT_VERSION=`rpm -qa | grep ${HOOT_RPM_PREFIX}`
# if a version of hoot is already install downgrade it
# else install the 2nd latest version of hootenanny
if [ ! -z ${INSTALLED_HOOT_VERSION} ]; then
    sudo yum -y downgrade ${HOOT_RPM_PREFIX}-${PREVIOUS_VERSION}
else
    sudo yum -y install ${HOOT_RPM_PREFIX}-${PREVIOUS_VERSION}
fi
