#!/bin/bash
# Copyright (C) 2018-2021 Maxar Technologies (https://www.maxar.com)
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
#  * VAGRANT_VERSION
#  * VAGRANT_BASEURL
LSB_DIST="$(. /etc/os-release && echo "${ID}")"
VAGRANT_VERSION="${VAGRANT_VERSION:-2.2.16}"
VAGRANT_BASEURL="${VAGRANT_BASEURL:-https://releases.hashicorp.com/vagrant/${VAGRANT_VERSION}}"

# Set up command differences between RHEL and Debian-based systems.
if [ "${LSB_DIST}" == "centos" ] || [ "${LSB_DIST}" == "fedora" ] || [ "${LSB_DIST}" == "rhel" ]; then
    # RHEL-based.
    if [ "$(rpm -q vagrant --queryformat '%{version}')" == "${VAGRANT_VERSION}" ]; then
        echo "Vagrant ${VAGRANT_VERSION} is already installed."
        exit 0
    fi
    DOWNLOAD_COMMAND="curl -sSL -O"
    INSTALL_COMMAND="yum install -y"
    PACKAGE_SUFFIX="$(arch).rpm"
elif [ "${LSB_DIST}" == "debian" ] || [ "${LSB_DIST}" == "ubuntu" ]; then
    # Debian-based.
    if [ "$(dpkg-query --showformat=\$\{Version\} --show vagrant)" == "1:${VAGRANT_VERSION}" ]; then
        echo "Vagrant ${VAGRANT_VERSION} is already installed."
        exit 0
    fi
    DOWNLOAD_COMMAND="wget -nv -L"
    INSTALL_COMMAND="dpkg -i"
    PACKAGE_SUFFIX="$(arch).deb"
else
    echo "Do not know how to install Vagrant on ${LSB_DIST}."
    exit 1
fi

if [ "$(id -u)" -ne 0 ]; then
    INSTALL_COMMAND="sudo ${INSTALL_COMMAND}"
fi

# Variables for package, checksum, and signature file.
PACKAGE="vagrant_${VAGRANT_VERSION}_${PACKAGE_SUFFIX}"
CHECKSUMS="vagrant_${VAGRANT_VERSION}_SHA256SUMS"
SIGNATURE="vagrant_${VAGRANT_VERSION}_SHA256SUMS.sig"

if [ ! -x /usr/bin/gpgv ]; then
    echo "Then gpgv utility is needed to verify ${PACKAGE}." >> /dev/stderr
    exit 1
fi

# Do all our file manipulation in temporary fs.
pushd /var/tmp

# Create Hashicorp GPG keyring from base64-encoded binary of the release
# key (C874 011F 0AB4 0511 0D02 1055 3436 5D94 72D7 468F).
echo "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" | \
    base64 -d > hashicorp.gpg

# Download Vagrant files.
for vagrant_file in ${PACKAGE} ${CHECKSUMS} ${SIGNATURE}; do
    ${DOWNLOAD_COMMAND} "${VAGRANT_BASEURL}/${vagrant_file}"
done

# GPG verify the signature for the SHA256SUMS file.
gpgv --keyring ./hashicorp.gpg "${SIGNATURE}" "${CHECKSUMS}"

# Verify checksums, but grep out all other lines in the checksum
# file except the desired package.
sha256sum -c <(grep -e "[[:space:]]\\+${PACKAGE}\\>" "${CHECKSUMS}")

# Finally install Vagrant.
${INSTALL_COMMAND} "${PACKAGE}"

# Clean up.
rm -f hashicorp.gpg "${PACKAGE}" "${CHECKSUMS}" "${SIGNATURE}"
popd
