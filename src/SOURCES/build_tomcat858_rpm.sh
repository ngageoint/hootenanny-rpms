#!/usr/bin/env bash

VERSION=$(grep "Version:" tomcat8.spec |cut -d ":" -f2 |tr -d "[:space:]")
RELEASE=$(grep "Release:" tomcat8.spec |cut -d ":" -f2 |tr -d "[:space:]")
ARCH=$(grep "BuildArch:" tomcat8.spec |cut -d ":" -f2 |tr -d "[:space:]")

echo "Version: $VERSION-$RELEASE BuildArch: $ARCH"

rm -rf rpmbuild
mkdir rpmbuild
mkdir rpmbuild/BUILD
mkdir rpmbuild/RPMS
mkdir rpmbuild/SOURCES
mkdir rpmbuild/SPECS
mkdir rpmbuild/SRPMS

ln -v -s "$(pwd)/apache-tomcat-$VERSION.tar.gz" "rpmbuild/SOURCES/"
ln -v -s "$(pwd)/tomcat8."{init,logrotate,sysconfig,bin,conf} "rpmbuild/SOURCES/"
ln -v -s "$(pwd)/tomcat8.spec" "rpmbuild/SPECS/"

cd rpmbuild

rpmbuild --buildroot "`pwd`/BUILDROOT" ../tomcat8.spec -bb --define "_topdir `pwd`"

publish-rpm $VERSION $RELEASE $ARCH tomcat8 "RPMS/$ARCH/tomcat8-$VERSION-$RELEASE.$ARCH.rpm"
