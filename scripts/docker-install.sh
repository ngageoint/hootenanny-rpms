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

# Allow overrides from environment for:
#  * DOCKER_BASEURL
#  * DOCKER_CHANNEL
LSB_DIST="$(. /etc/os-release && echo "$ID")"
DOCKER_BASEURL="${DOCKER_BASEURL:-https://download.docker.com/linux/$LSB_DIST}"
DOCKER_CHANNEL="${DOCKER_CHANNEL:-stable}"

if [ "$LSB_DIST" == 'centos' -o "$LSB_DIST" == 'fedora' -o "$LSB_DIST" == 'rhel' ]; then
    # Configure Docker yum repository with `yum-config-manager`.
    sudo yum install -q -y yum-utils
    sudo yum-config-manager --add-repo "$DOCKER_BASEURL/docker-ce.repo"
    sudo yum-config-manager --enable "docker-ce-$DOCKER_CHANNEL"

    # Install Docker.
    sudo yum makecache
    sudo yum install -q -y docker-ce
elif [ "$LSB_DIST" == 'debian' -o "$LSB_DIST" == 'ubuntu' ]; then
    # Install prerequisite packages to access apt over https.
    sudo apt-get update -qq >/dev/null
    sudo apt-get install -qq -y apt-transport-https ca-certificates curl gnupg

    # Configure Docker apt repository.
    DPKG_ARCH="$(dpkg --print-architecture)"
    VERSION_CODENAME="$(. /etc/os-release && echo "$VERSION_CODENAME")"
    sudo bash -c "cat > /etc/apt/sources.list.d/docker.list" <<EOF
deb [arch=$DPKG_ARCH] $DOCKER_BASEURL $VERSION_CODENAME $DOCKER_CHANNEL
EOF
    curl -fsSL "$DOCKER_BASEURL/gpg" | sudo apt-key add -qq - >/dev/null

    # Install Docker.
    sudo apt-get update -qq >/dev/null
    sudo apt-get install -y -qq --no-install-recommends docker-ce
else
    echo "Do not know how to install docker on $LSB_DIST."
    exit 1
fi

# Enable and start the Docker service
sudo systemctl enable docker
sudo systemctl start docker

# Modify invoking user to be apart of the `docker` group.
sudo usermod -a -G docker "$USER"
