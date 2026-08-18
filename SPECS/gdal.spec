Name:           gdal
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Geospatial Data Abstraction Library

Group:          Development/Libraries
License:        MIT
URL:            https://gdal.org
Source0:        https://github.com/OSGeo/gdal/archive/refs/tags/v%{version}.tar.gz
Requires:       FileGDBAPI

%global __cmake_builddir build
%global _smp_mflags -j%(nproc)

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  proj-devel
BuildRequires:  geos-devel
BuildRequires:  sqlite-devel
BuildRequires:  libcurl-devel
BuildRequires:  libxml2-devel
BuildRequires:  expat-devel
BuildRequires:  zlib-devel
BuildRequires:  libtiff-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  libkml-devel
BuildRequires:  FileGDBAPI-devel

%description
GDAL is a translator library for raster and vector geospatial data
formats, built with LIBKML and FileGDB driver support enabled.

%package devel
Group:          Development/Libraries
Summary:        Development files for %{name}
Requires:       %{name}%{_isa} = %{version}-%{release}

%description devel
Development headers and libraries for %{name}.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%cmake -S . -B build \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_TESTING=OFF \
    -DGDAL_USE_LIBKML=ON \
    -DGDAL_USE_FILEGDB=ON
%cmake_build

%install
%cmake_install

%files
%license LICENSE.TXT
%{_libdir}/*.so.*
%{_bindir}/gdal*
%{_bindir}/ogr*
%{_bindir}/gnm*
%{_bindir}/nearblack
%{_bindir}/sozip
%{_libdir}/gdalplugins
%{_datadir}/bash-completion
%{_datadir}/gdal

%files devel
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/gdal

%changelog
* Wed Aug 19 2026 Leia <leia@vantor.com> - 3.10.3-1
- Initial RHEL 9 / Rocky 9 spec with LIBKML and FileGDB drivers enabled.
