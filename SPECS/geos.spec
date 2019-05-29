Name:		geos
Version:	%{rpmbuild_version}
Release:	%{rpmbuild_release}%{?dist}
Summary:	GEOS is a C++ port of the Java Topology Suite

License:	LGPLv2
URL:		http://trac.osgeo.org/geos/
Source0:	http://download.osgeo.org/%{name}/%{name}-%{version}.tar.bz2

BuildRequires:	doxygen
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	libtool

%description
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid().

%package devel
Summary:	Development files for GEOS
Requires: 	%{name} = %{version}-%{release}

%description devel
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid().

This package contains the development files to build applications that
use GEOS.

%prep
%setup -q

%build

# disable internal libtool to avoid hardcoded r-path
for makefile in `find . -type f -name 'Makefile.in'`; do
sed -i 's|@LIBTOOL@|%{_bindir}/libtool|g' $makefile
done

%configure --disable-static --disable-dependency-tracking
make %{?_smp_mflags}

# Make doxygen documentation files
cd doc
make doxygen-html

%install
%{__rm} -rf %{buildroot}
make DESTDIR=%{buildroot} install

%check

# test module
make %{?_smp_mflags} check || exit 0

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING NEWS README.md TODO
%{_libdir}/libgeos-%{version}.so
%{_libdir}/libgeos_c.so.1*
%exclude %{_libdir}/*.a

%files devel
%doc doc/doxygen_docs
%{_bindir}/geos-config
%{_includedir}/*
%{_libdir}/libgeos.so
%{_libdir}/libgeos_c.so
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.a

%changelog
* Wed Nov 29 2017 Justin Bronn <justin.bronn@digitalglobe.com> - 3.6.2-1
- Upgrade to 3.6.2.
* Wed Nov 15 2017 Justin Bronn <justin.bronn@digitalglobe.com> - 3.6.1-1
- Initial release for use with Hootenanny.
