Name:           libkml
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Library to parse, generate, and operate on KML

Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/libkml/libkml
Source0:        https://github.com/libkml/libkml/archive/refs/tags/%{version}.tar.gz
%global __cmake_builddir build

%global _smp_mflags -j%(nproc)

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  boost-devel
BuildRequires:  expat-devel
BuildRequires:  zlib-devel
BuildRequires:  minizip1.2-devel
BuildRequires:  uriparser-devel

%description
libkml is a library to parse, generate, and operate on KML, the
XML-based language for expressing geographic annotation and
visualization within Internet-based two- and three-dimensional maps.

%package devel
Group:          Development/Libraries
Summary:        Development files for %{name}
Requires:       %{name}%{_isa} = %{version}-%{release}

%description devel
Development headers and libraries for %{name}.

%prep
%autosetup -n %{name}-%{version} -p1
sed -i "1i #define NOUNCRYPT" src/kml/base/contrib/minizip/unzip.c
sed -i "/#undef NOUNCRYPT/d" src/kml/base/contrib/minizip/unzip.c

%build
%cmake -S . -B build \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_TESTING=OFF \
    -DBUILD_EXAMPLES=OFF \
    -DINCLUDE_INSTALL_DIR=/usr/include/kml
%cmake_build

%install
%cmake_install

%files
%license COPYING LICENSE
%doc README.md NEWS
%{_libdir}/*.so.*

%files devel
%{_includedir}/kml/base
%{_includedir}/kml/convenience
%{_includedir}/kml/dom
%{_includedir}/kml/dom.h
%{_includedir}/kml/engine
%{_includedir}/kml/engine.h
%{_includedir}/kml/regionator
%{_includedir}/kml/xsd
%{_libdir}/*.so
/usr/lib/cmake/%{name}
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Aug 19 2026 Leia <leia@vantor.com> - 1.3.0-1
- Initial RHEL 9 / Rocky 9 spec.
