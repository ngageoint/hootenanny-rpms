%global datumgrid_version 1.8

# Major digit of the proj shared library version.
%global proj_somaj 15

Name:           proj
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Cartographic projection software (PROJ.4)
License:        MIT
URL:            https://proj4.org
Source0:        https://github.com/OSGeo/proj.4/releases/download/%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/OSGeo/proj-datumgrid/releases/download/%{datumgrid_version}/proj-datumgrid-%{datumgrid_version}.tar.gz

BuildRequires:  libtool
BuildRequires:  gcc-c++
BuildRequires:  sqlite-devel

Provides:       proj-epsg = %{version}-%{release}
Requires:       proj-datumgrid = %{datumgrid_version}-%{release}

%description
Proj and invproj perform respective forward and inverse transformation of
cartographic data to or from cartesian data with a wide range of selectable
projection functions.


%package devel
Summary:        Development files for PROJ.4
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains libproj and the appropriate header files and man pages.


%package static
Summary:        Development files for PROJ.4
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
This package contains libproj static library.


%package datumgrid
Summary:        Additional datum shift grids for PROJ.4
Version:        %{datumgrid_version}
# See README.DATUMGRID
License:        CC-BY and Freely Distributable and Ouverte and Public Domain
BuildArch:      noarch

Provides:       proj-nad = %{version}-%{release}

%description datumgrid
This package contains additional datum shift grids.


%prep
%autosetup -p1

# Prepare datumgrid and file list (in {datadir}/proj and README marked as doc)
tar xvf %{SOURCE1} -C data | \
    sed -e 's!^!%{_datadir}/%{name}/!' -e '/README/s!^!%%doc !' > datumgrid.files


%build
# rebuild due to patch
autoreconf -i
%configure
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build


%install
%make_install
chmod -x %{buildroot}%{_libdir}/libproj.la
install -p -m 0644 data/README.DATUMGRID %{buildroot}%{_datadir}/%{name}


# Install cmake config manually because we use autotools for building
mkdir -p %{buildroot}%{_datadir}/cmake/Modules/

cat << EOF > %{buildroot}%{_datadir}/cmake/Modules/FindPROJ4.cmake
set(PROJ4_FOUND 1)
set(PROJ4_INCLUDE_DIRS %{_includedir})
set(PROJ4_LIBRARIES proj)
if(\${LIB_SUFFIX} MATCHES 64)
set(PROJ4_LIBRARY_DIRS /usr/lib64)
else()
set(PROJ4_LIBRARY_DIRS /usr/lib)
endif()
set(PROJ4_BINARY_DIRS %{_bindir})
set(PROJ4_VERSION %{version})
message(STATUS "Found PROJ4: version \${PROJ4_VERSION}")
EOF


%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} \
    make PROJ_LIB=%{buildroot}%{_datadir}/%{name} check || ( cat src/test-suite.log; exit 1 )


%files
%doc NEWS AUTHORS COPYING README ChangeLog
%{_bindir}/*
%{_mandir}/man1/*.1*
%{_libdir}/libproj.so.%{proj_somaj}*
%{_datadir}/%{name}/CH
%{_datadir}/%{name}/GL27
%{_datadir}/%{name}/ITRF2000
%{_datadir}/%{name}/ITRF2008
%{_datadir}/%{name}/ITRF2014
%{_datadir}/%{name}/nad.lst
%{_datadir}/%{name}/nad27
%{_datadir}/%{name}/nad83
%{_datadir}/%{name}/null
%{_datadir}/%{name}/other.extra
%{_datadir}/%{name}/proj.db
%{_datadir}/%{name}/world

%files devel
%{_mandir}/man3/*.3*
%{_includedir}/*.h
%{_includedir}/%{name}/*.hpp
%{_libdir}/libproj.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/cmake/Modules/FindPROJ4.cmake
%exclude %{_libdir}/libproj.a
%exclude %{_libdir}/libproj.la

%files static
%{_libdir}/libproj.a
%{_libdir}/libproj.la

%files datumgrid -f datumgrid.files
%dir %{_datadir}/%{name}


%changelog
* Fri May 17 2019 Justin Bronn <justin.bronn@radiantsolutions.com> - 6.1.0-1
- Initial Release: 6.1.0
