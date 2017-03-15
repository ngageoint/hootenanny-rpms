####
### This is far from complete. Just playing.
####
Name:		FileGDB_API
Version:	1.5
Release:	1%{?dist}
Summary:	ESRI FileGDB libraries

Group:		System Environment/Libraries
License:	Copyright © 2012 ESRI
URL:		http://www.esri.com/apps/products/download/#File_Geodatabase_API_1.4

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source1:        FileGDB_API_1_5_64.tar.gz

%description

Copyright © 2012 ESRI

All rights reserved under the copyright laws of the United States and
applicable international laws, treaties, and conventions.

You may freely redistribute and use the sample code, with or without
modification, provided you include the original copyright notice and use
restrictions.

Disclaimer:  THE SAMPLE CODE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL ESRI OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) SUSTAINED BY YOU OR A THIRD PARTY, HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
TORT ARISING IN ANY WAY OUT OF THE USE OF THIS SAMPLE CODE, EVEN IF ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.

For additional information, contact:
Environmental Systems Research Institute, Inc.
Attn: Contracts and Legal Services Department
380 New York Street
Redlands, California, 92373
USA

email: contracts@esri.com


%files
%{_includedir}/*
%{_libdir}/*
/usr/share/*

%prep
mkdir -p %{name}-%{version}/FileGDB_API
cd %{name}-%{version}/FileGDB_API
tar xf %{_sourcedir}/FileGDB_API_1_5_64.tar.gz --strip-components 1

%build
true

%install
rm -rf $RPM_BUILD_ROOT
export BUILD_DIR=$RPM_BUILD_DIR/$RPM_PACKAGE_NAME-$RPM_PACKAGE_VERSION/FileGDB_API
export INSTALL_DIR=$RPM_BUILD_ROOT/usr/
export SHARE_DIR=$INSTALL_DIR/share/filegdb/
export LIB_DIR=$INSTALL_DIR/lib64/
install -d $INSTALL_DIR
install -d $SHARE_DIR
install -d $LIB_DIR
install -d $INSTALL_DIR/include

cp -R $BUILD_DIR/doc/ $SHARE_DIR/
install -D $BUILD_DIR/license/* $SHARE_DIR/
install -D $BUILD_DIR/lib/* $LIB_DIR
install -D $BUILD_DIR/include/* $INSTALL_DIR/include/

%check

%clean

%changelog
* Tue Mar 07 2017 Benjamin Marchant <benjamin.marchant@digitalglobe.com>
- Upgrade to v1.5
* Thu Jan 19 2017 Benjamin Marchant <benjamin.marchant@digitalglobe.com>
- Upgrade to v1.4
* Thu Jan 26 2016 Jason R. Surratt <jason.surratt@digitalglobe.com>
- Initial attempt
