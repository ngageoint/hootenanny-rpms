#!/bin/bash
set -euxo pipefail

# Allow overrides from environment for:
#  * VAGRANT_VERSION
#  * VAGRANT_BASEURL
LSB_DIST="$(. /etc/os-release && echo "$ID")"
VAGRANT_VERSION="${VAGRANT_VERSION:-2.1.1}"
VAGRANT_BASEURL="${VAGRANT_BASEURL:-https://releases.hashicorp.com/vagrant/$VAGRANT_VERSION}"

# Set up command differences between RHEL and Debian-based systems.
if [ "$LSB_DIST" == 'centos' -o "$LSB_DIST" == 'fedora' -o "$LSB_DIST" == 'rhel' ]; then
    # RHEL-based.
    if [ "$(rpm -q vagrant --queryformat '%{version}')" == "$VAGRANT_VERSION" ]; then
        echo "Vagrant $VAGRANT_VERSION is already installed."
        exit 0
    fi
    DOWNLOAD_COMMAND='curl -sSL -O'
    INSTALL_COMMAND='sudo yum install -y'
    PACKAGE_SUFFIX=x86_64.rpm
elif [ "$LSB_DIST" == 'debian' -o "$LSB_DIST" == 'ubuntu' ]; then
    # Debian-based.
    if [ "$(dpkg-query --showformat=\$\{Version\} --show vagrant)" == "1:$VAGRANT_VERSION" ]; then
        echo "Vagrant $VAGRANT_VERSION is already installed."
        exit 0
    fi
    DOWNLOAD_COMMAND='wget -nv -L'
    INSTALL_COMMAND='sudo dpkg -i'
    PACKAGE_SUFFIX=x86_64.deb
else
    echo "Do not know how to install Vagrant on $LSB_DIST."
    exit 1
fi

# Variables for package, checksum, and signature file.
PACKAGE="vagrant_${VAGRANT_VERSION}_${PACKAGE_SUFFIX}"
CHECKSUMS="vagrant_${VAGRANT_VERSION}_SHA256SUMS"
SIGNATURE="vagrant_${VAGRANT_VERSION}_SHA256SUMS.sig"

# Do all our file manipulation in temporary fs.
pushd /var/tmp

# Import Hashicorp key.
if ! gpg --list-public-keys --with-colons | \
        awk -F: '{ print $5 }' | \
        grep -q '^51852D87348FFC4C\>'; then
    cat > hashicorp.key <<EOF
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1

mQENBFMORM0BCADBRyKO1MhCirazOSVwcfTr1xUxjPvfxD3hjUwHtjsOy/bT6p9f
W2mRPfwnq2JB5As+paL3UGDsSRDnK9KAxQb0NNF4+eVhr/EJ18s3wwXXDMjpIifq
fIm2WyH3G+aRLTLPIpscUNKDyxFOUbsmgXAmJ46Re1fn8uKxKRHbfa39aeuEYWFA
3drdL1WoUngvED7f+RnKBK2G6ZEpO+LDovQk19xGjiMTtPJrjMjZJ3QXqPvx5wca
KSZLr4lMTuoTI/ZXyZy5bD4tShiZz6KcyX27cD70q2iRcEZ0poLKHyEIDAi3TM5k
SwbbWBFd5RNPOR0qzrb/0p9ksKK48IIfH2FvABEBAAG0K0hhc2hpQ29ycCBTZWN1
cml0eSA8c2VjdXJpdHlAaGFzaGljb3JwLmNvbT6JATgEEwECACIFAlMORM0CGwMG
CwkIBwMCBhUIAgkKCwQWAgMBAh4BAheAAAoJEFGFLYc0j/xMyWIIAIPhcVqiQ59n
Jc07gjUX0SWBJAxEG1lKxfzS4Xp+57h2xxTpdotGQ1fZwsihaIqow337YHQI3q0i
SqV534Ms+j/tU7X8sq11xFJIeEVG8PASRCwmryUwghFKPlHETQ8jJ+Y8+1asRydi
psP3B/5Mjhqv/uOK+Vy3zAyIpyDOMtIpOVfjSpCplVRdtSTFWBu9Em7j5I2HMn1w
sJZnJgXKpybpibGiiTtmnFLOwibmprSu04rsnP4ncdC2XRD4wIjoyA+4PKgX3sCO
klEzKryWYBmLkJOMDdo52LttP3279s7XrkLEE7ia0fXa2c12EQ0f0DQ1tGUvyVEW
WmJVccm5bq25AQ0EUw5EzQEIANaPUY04/g7AmYkOMjaCZ6iTp9hB5Rsj/4ee/ln9
wArzRO9+3eejLWh53FoN1rO+su7tiXJA5YAzVy6tuolrqjM8DBztPxdLBbEi4V+j
2tK0dATdBQBHEh3OJApO2UBtcjaZBT31zrG9K55D+CrcgIVEHAKY8Cb4kLBkb5wM
skn+DrASKU0BNIV1qRsxfiUdQHZfSqtp004nrql1lbFMLFEuiY8FZrkkQ9qduixo
mTT6f34/oiY+Jam3zCK7RDN/OjuWheIPGj/Qbx9JuNiwgX6yRj7OE1tjUx6d8g9y
0H1fmLJbb3WZZbuuGFnK6qrE3bGeY8+AWaJAZ37wpWh1p0cAEQEAAYkBHwQYAQIA
CQUCUw5EzQIbDAAKCRBRhS2HNI/8TJntCAClU7TOO/X053eKF1jqNW4A1qpxctVc
z8eTcY8Om5O4f6a/rfxfNFKn9Qyja/OG1xWNobETy7MiMXYjaa8uUx5iFy6kMVaP
0BXJ59NLZjMARGw6lVTYDTIvzqqqwLxgliSDfSnqUhubGwvykANPO+93BBx89MRG
unNoYGXtPlhNFrAsB1VR8+EyKLv2HQtGCPSFBhrjuzH3gxGibNDDdFQLxxuJWepJ
EK1UbTS4ms0NgZ2Uknqn1WRU1Ki7rE4sTy68iZtWpKQXZEJa0IGnuI2sSINGcXCJ
oEIgXTMyCILo34Fa/C6VCm2WBgz9zZO8/rHIiQm1J5zqz0DrDwKBUM9C
=LYpS
-----END PGP PUBLIC KEY BLOCK-----
EOF
    gpg --import < hashicorp.key
    rm hashicorp.key
fi

# Download Vagrant files.
for vagrant_file in $PACKAGE $CHECKSUMS $SIGNATURE
do
    $DOWNLOAD_COMMAND "$VAGRANT_BASEURL/$vagrant_file"
done

# GPG verify the signature for the SHA256SUMS file.
gpg --verify "$SIGNATURE"

# Verify checksums, but grep out all other lines in the checksum
# file except the desired package.
sha256sum -c <(grep -e "[[:space:]]\\+$PACKAGE\\>" "$CHECKSUMS")

# Finally install Vagrant.
$INSTALL_COMMAND "$PACKAGE"

# Clean up.
rm -f "$PACKAGE" "$CHECKSUMS" "$SIGNATURE"
popd
