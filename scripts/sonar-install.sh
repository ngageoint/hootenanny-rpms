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

# Main sonar scanner
SONAR_VERSION=3.1.0.1141
SONAR_CLI=sonar-scanner-cli-$SONAR_VERSION-linux
SONAR_PKG=sonar-scanner-$SONAR_VERSION-linux
SONAR_ZIP=$SONAR_CLI.zip
SONAR_URL=https://binaries.sonarsource.com/Distribution/sonar-scanner-cli
SONAR_PATH=/opt/sonar

# Sonar build wrapper (required to scan C/C++)
SONAR_BLD_PKG=build-wrapper-linux-x86
SONAR_BLD_ZIP=$SONAR_BLD_PKG.zip
SONAR_BLD_URL=https://sonarcloud.io/static/cpp

# Do everything in temporary folder.
pushd /var/tmp

echo "### Downloading Sonar Scanner..."
su-exec "$RPMBUILD_USER" curl -sSL -O $SONAR_URL/$SONAR_ZIP

echo "### Installing Sonar Scanner..."
su-exec "$RPMBUILD_USER" unzip -qq -o $SONAR_ZIP
chown -R root:root $SONAR_PKG
mv $SONAR_PKG $SONAR_PATH

# Add the sonar binaries to the system profile $PATH.
echo "pathmunge $SONAR_PATH/bin after" > /etc/profile.d/sonarqube.sh

echo "### Downloading Sonar Build Wrapper..."
su-exec "$RPMBUILD_USER" curl -sSL -O $SONAR_BLD_URL/$SONAR_BLD_ZIP

echo "### Installing Sonar Build Wrapper..."
su-exec "$RPMBUILD_USER" unzip -qq -o $SONAR_BLD_ZIP
chown -R root:root $SONAR_BLD_PKG
mv $SONAR_BLD_PKG/$SONAR_BLD_PKG-64 $SONAR_PATH/bin/
mv $SONAR_BLD_PKG/libinterceptor-x86_64.so $SONAR_PATH/bin/
mv $SONAR_BLD_PKG/libinterceptor-i686.so $SONAR_PATH/bin/

echo "### Cleaning Up..."
rm -rf $SONAR_BLD_PKG $SONAR_ZIP $SONAR_BLD_ZIP

popd
