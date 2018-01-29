## ESRI File Geodatabase API Library
%global debug_package %{nil}

Name:		FileGDBAPI
Version:	1.5.1
Release:	1%{?dist}
Summary:	ESRI FileGDB API
Group:		System Environment/Libraries
License:	ASL 2.0
URL:		https://github.com/Esri/file-geodatabase-api
Source0:	https://github.com/Esri/file-geodatabase-api/raw/master/FileGDB_API_%{version}/FileGDB_API_%(echo %{version} | tr '.' '_')-64.tar.gz

%description
The FileGDB API provides basic tools that allow the creation of file
geodatbases, feature classes and tables. Simple features can be created
and loaded.

Copyright © 2014 ESRI

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
%{_libdir}/libFileGDBAPI.so
%{_libdir}/libfgdbunixrtl.so

#%files devel
%{_includedir}/%{name}/*
%{_libdir}/libfgdbunixrtl.a
%{_libdir}/pkgconfig/%{name}.pc

#%files doc
%{_datarootdir}/doc/%{name}-%{version}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%prep
%setup -q -n FileGDB_API-64

%build

%install
%{__install} -d %{buildroot}%{_libdir}
%{__install} -d %{buildroot}%{_includedir}/%{name}
%{__install} -d %{buildroot}%{_libdir}/pkgconfig
%{__install} -d %{buildroot}%{_datarootdir}/doc/%{name}-%{version}/FileGDB_SQL_files

# TODO: Version dynamic libs?
%{__install} -m 0755 -D %{_builddir}/FileGDB_API-64/lib/libFileGDBAPI.so %{buildroot}%{_libdir}/libFileGDBAPI.so
%{__install} -m 0755 -D %{_builddir}/FileGDB_API-64/lib/libfgdbunixrtl.so %{buildroot}%{_libdir}/libfgdbunixrtl.so

# devel
%{__install} -m 0644 -D %{_builddir}/FileGDB_API-64/lib/libfgdbunixrtl.a %{buildroot}%{_libdir}
%{__install} -m 0644 -D %{_builddir}/FileGDB_API-64/include/* %{buildroot}%{_includedir}/%{name}

# doc
%{__install} -m 0644 -D %{_builddir}/FileGDB_API-64/doc/html/*.{css,html,js,pdf,png,txt,xml} %{buildroot}%{_datarootdir}/doc/%{name}-%{version}
%{__install} -m 0644 -D %{_builddir}/FileGDB_API-64/doc/html/FileGDB_SQL_files/*.xml %{buildroot}%{_datarootdir}/doc/%{name}-%{version}/FileGDB_SQL_files

%{__cat} > %{buildroot}%{_libdir}/pkgconfig/%{name}.pc <<EOF
prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/%{name}

Name: %{name}
Description: ESRI FileGDB API
Version: %{version}
Cflags: -I\${includedir}
EOF
%{__chmod} 0644 %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

%check

%clean

%changelog
* Wed Nov 15 2017 Justin Bronn <justin.bronn@digitalglobe.com> - 1.5.1-1
- Upgrade to v1.5.1, refactor spec file, and add pkg-config support.
* Tue Mar 07 2017 Benjamin Marchant <benjamin.marchant@digitalglobe.com>
- Upgrade to v1.5
* Thu Jan 19 2017 Benjamin Marchant <benjamin.marchant@digitalglobe.com>
- Upgrade to v1.4
* Tue Jan 26 2016 Jason R. Surratt <jason.surratt@digitalglobe.com>
- Initial attempt
