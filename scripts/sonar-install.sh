#!/bin/bash
set -euo pipefail

# Main sonar scanner
SONAR_VERSION=3.1.0.1141
SONAR_CLI=sonar-scanner-cli-$SONAR_VERSION-linux
SONAR_PKG=sonar-scanner-$SONAR_VERSION-linux
SONAR_ZIP=$SONAR_CLI.zip
SONAR_URL=https://sonarsource.bintray.com/Distribution/sonar-scanner-cli
SONAR_PATH=/opt/sonar

# Sonar build wrapper (required to scan C/C++)
SONAR_BLD_PKG=build-wrapper-linux-x86
SONAR_BLD_ZIP=$SONAR_BLD_PKG.zip
SONAR_BLD_URL=https://sonarcloud.io/static/cpp

# Do everything in temporary folder.
pushd /var/tmp

echo "### Downloading Sonar Scanner..."
su-exec $RPMBUILD_USER curl -sSL -O $SONAR_URL/$SONAR_ZIP

echo "### Installing Sonar Scanner..."
su-exec $RPMBUILD_USER unzip -qq -o $SONAR_ZIP
chown -R root:root $SONAR_PKG
mv $SONAR_PKG $SONAR_PATH

# Add the sonar binaries to the system profile $PATH.
echo "pathmunge $SONAR_PATH/bin after" > /etc/profile.d/sonarqube.sh

echo "### Downloading Sonar Build Wrapper..."
su-exec $RPMBUILD_USER curl -sSL -O $SONAR_BLD_URL/$SONAR_BLD_ZIP

echo "### Installing Sonar Build Wrapper..."
su-exec $RPMBUILD_USER unzip -qq -o $SONAR_BLD_ZIP
chown -R root:root $SONAR_BLD_PKG
mv $SONAR_BLD_PKG/$SONAR_BLD_PKG-64 $SONAR_PATH/bin/
mv $SONAR_BLD_PKG/libinterceptor-x86_64.so $SONAR_PATH/bin/
mv $SONAR_BLD_PKG/libinterceptor-i686.so $SONAR_PATH/bin/

echo "### Cleaning Up..."
rm -rf $SONAR_BLD_PKG $SONAR_ZIP $SONAR_BLD_ZIP

popd
