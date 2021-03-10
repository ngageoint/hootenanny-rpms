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
LSB_DIST="$(. /etc/os-release && echo "$ID")"
VAGRANT_VERSION="${VAGRANT_VERSION:-2.2.14}"
VAGRANT_BASEURL="${VAGRANT_BASEURL:-https://releases.hashicorp.com/vagrant/$VAGRANT_VERSION}"

# Set up command differences between RHEL and Debian-based systems.
if [ "$LSB_DIST" == 'centos' -o "$LSB_DIST" == 'fedora' -o "$LSB_DIST" == 'rhel' ]; then
    # RHEL-based.
    if [ "$(rpm -q vagrant --queryformat '%{version}')" == "$VAGRANT_VERSION" ]; then
        echo "Vagrant $VAGRANT_VERSION is already installed."
        exit 0
    fi
    DOWNLOAD_COMMAND='curl -sSL -O'
    INSTALL_COMMAND='yum install -y'
    PACKAGE_SUFFIX="$(arch).rpm"
elif [ "$LSB_DIST" == 'debian' -o "$LSB_DIST" == 'ubuntu' ]; then
    # Debian-based.
    if [ "$(dpkg-query --showformat=\$\{Version\} --show vagrant)" == "1:$VAGRANT_VERSION" ]; then
        echo "Vagrant $VAGRANT_VERSION is already installed."
        exit 0
    fi
    DOWNLOAD_COMMAND='wget -nv -L'
    INSTALL_COMMAND='dpkg -i'
    PACKAGE_SUFFIX="$(arch).deb"
else
    echo "Do not know how to install Vagrant on $LSB_DIST."
    exit 1
fi

if [ "$(id -u)" -ne 0 ]; then
    INSTALL_COMMAND="sudo $INSTALL_COMMAND"
fi

# Variables for package, checksum, and signature file.
PACKAGE="vagrant_${VAGRANT_VERSION}_${PACKAGE_SUFFIX}"
CHECKSUMS="vagrant_${VAGRANT_VERSION}_SHA256SUMS"
SIGNATURE="vagrant_${VAGRANT_VERSION}_SHA256SUMS.sig"

if [ ! -x /usr/bin/gpgv ]; then
    echo "Then gpgv utility is needed to verify $PACKAGE." >> /dev/stderr
    exit 1
fi

# Do all our file manipulation in temporary fs.
pushd /var/tmp

# Create Hashicorp GPG keyring from base64-encoded binary of the release
# key (91A6E7F85D05C65630BEF18951852D87348FFC4C).
if [ ! -f hashicorp.gpg ]; then
echo "mQENBFMORM0BCADBRyKO1MhCirazOSVwcfTr1xUxjPvfxD3hjUwHtjsOy/bT6p9fW2mRPfwnq2JB
5As+paL3UGDsSRDnK9KAxQb0NNF4+eVhr/EJ18s3wwXXDMjpIifqfIm2WyH3G+aRLTLPIpscUNKD
yxFOUbsmgXAmJ46Re1fn8uKxKRHbfa39aeuEYWFA3drdL1WoUngvED7f+RnKBK2G6ZEpO+LDovQk
19xGjiMTtPJrjMjZJ3QXqPvx5wcaKSZLr4lMTuoTI/ZXyZy5bD4tShiZz6KcyX27cD70q2iRcEZ0
poLKHyEIDAi3TM5kSwbbWBFd5RNPOR0qzrb/0p9ksKK48IIfH2FvABEBAAG0K0hhc2hpQ29ycCBT
ZWN1cml0eSA8c2VjdXJpdHlAaGFzaGljb3JwLmNvbT6JATgEEwECACIFAlMORM0CGwMGCwkIBwMC
BhUIAgkKCwQWAgMBAh4BAheAAAoJEFGFLYc0j/xMyWIIAIPhcVqiQ59nJc07gjUX0SWBJAxEG1lK
xfzS4Xp+57h2xxTpdotGQ1fZwsihaIqow337YHQI3q0iSqV534Ms+j/tU7X8sq11xFJIeEVG8PAS
RCwmryUwghFKPlHETQ8jJ+Y8+1asRydipsP3B/5Mjhqv/uOK+Vy3zAyIpyDOMtIpOVfjSpCplVRd
tSTFWBu9Em7j5I2HMn1wsJZnJgXKpybpibGiiTtmnFLOwibmprSu04rsnP4ncdC2XRD4wIjoyA+4
PKgX3sCOklEzKryWYBmLkJOMDdo52LttP3279s7XrkLEE7ia0fXa2c12EQ0f0DQ1tGUvyVEWWmJV
ccm5bq25AQ0EUw5EzQEIANaPUY04/g7AmYkOMjaCZ6iTp9hB5Rsj/4ee/ln9wArzRO9+3eejLWh5
3FoN1rO+su7tiXJA5YAzVy6tuolrqjM8DBztPxdLBbEi4V+j2tK0dATdBQBHEh3OJApO2UBtcjaZ
BT31zrG9K55D+CrcgIVEHAKY8Cb4kLBkb5wMskn+DrASKU0BNIV1qRsxfiUdQHZfSqtp004nrql1
lbFMLFEuiY8FZrkkQ9qduixomTT6f34/oiY+Jam3zCK7RDN/OjuWheIPGj/Qbx9JuNiwgX6yRj7O
E1tjUx6d8g9y0H1fmLJbb3WZZbuuGFnK6qrE3bGeY8+AWaJAZ37wpWh1p0cAEQEAAYkBHwQYAQIA
CQUCUw5EzQIbDAAKCRBRhS2HNI/8TJntCAClU7TOO/X053eKF1jqNW4A1qpxctVcz8eTcY8Om5O4
f6a/rfxfNFKn9Qyja/OG1xWNobETy7MiMXYjaa8uUx5iFy6kMVaP0BXJ59NLZjMARGw6lVTYDTIv
zqqqwLxgliSDfSnqUhubGwvykANPO+93BBx89MRGunNoYGXtPlhNFrAsB1VR8+EyKLv2HQtGCPSF
BhrjuzH3gxGibNDDdFQLxxuJWepJEK1UbTS4ms0NgZ2Uknqn1WRU1Ki7rE4sTy68iZtWpKQXZEJa
0IGnuI2sSINGcXCJoEIgXTMyCILo34Fa/C6VCm2WBgz9zZO8/rHIiQm1J5zqz0DrDwKBUM9C" | \
    base64 -d > hashicorp.gpg
fi

# Download Vagrant files.
for vagrant_file in $PACKAGE $CHECKSUMS $SIGNATURE
do
    $DOWNLOAD_COMMAND "$VAGRANT_BASEURL/$vagrant_file"
done

# GPG verify the signature for the SHA256SUMS file.
gpgv --keyring ./hashicorp.gpg "$SIGNATURE" "$CHECKSUMS"

# Verify checksums, but grep out all other lines in the checksum
# file except the desired package.
sha256sum -c <(grep -e "[[:space:]]\\+$PACKAGE\\>" "$CHECKSUMS")

# Finally install Vagrant.
$INSTALL_COMMAND "$PACKAGE"

# Clean up.
rm -f hashicorp.gpg "$PACKAGE" "$CHECKSUMS" "$SIGNATURE"
popd
