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

# Download sonar scanner
if [ ! -f $SONAR_ZIP ]; then
    echo "### Downloading Sonar Scanner..."
    curl -sSL -O $SONAR_URL/$SONAR_ZIP
fi

# Install sonar scanner
if [ ! -f $SONAR_PATH ]; then
    echo "### Installing Sonar Scanner..."
    if [ ! -f $SONAR_PKG ]; then
        unzip -qq -o $SONAR_ZIP
    fi
    mv $SONAR_PKG $SONAR_PATH
    echo "pathmunge $SONAR_PATH/bin after" > /etc/profile.d/sonarqube.sh
fi

# Download sonar build wrapper
if [ ! -f $SONAR_BLD_ZIP ]; then
    echo "### Downloading Sonar Build Wrapper..."
    curl -sSL -O $SONAR_BLD_URL/$SONAR_BLD_ZIP
fi

#Install sonar build wrapper
if [ ! -f $SONAR_PATH/bin/$SONAR_BLD_PKG-64 ]; then
    echo "### Installing Sonar Build Wrapper..."
    if [ ! -f $SONAR_BLD_PKG ]; then
        unzip -qq -o $SONAR_BLD_ZIP
    fi
    mv $SONAR_BLD_PKG/$SONAR_BLD_PKG-64 $SONAR_PATH/bin/
    mv $SONAR_BLD_PKG/libinterceptor-x86_64.so $SONAR_PATH/bin/
    mv $SONAR_BLD_PKG/libinterceptor-i686.so $SONAR_PATH/bin/
    rm -rf $SONAR_BLD_PKG
fi
