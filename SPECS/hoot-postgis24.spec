%global postgis_major %(echo %{rpmbuild_version} | awk -F. '{ print $1 }')
%global postgis_minor %(echo %{rpmbuild_version} | awk -F. '{ print $2 }')
%global postgis_micro %(echo %{rpmbuild_version} | awk -F. '{ print $3 }')
%global postgismajorversion %{postgis_major}.%{postgis_minor}
%global postgiscurrmajorversion %(echo %{postgismajorversion}|tr -d '.')
%global postgisprevmajorversion 2.3
%global sname hoot-postgis

%{!?utils:%global	utils 1}
%if 0%{?fedora} >= 24 || 0%{?rhel} >= 6 || 0%{?suse_version} >= 1315
%{!?raster:%global     raster 1}
%else
%{!?raster:%global     raster 0}
%endif
%if 0%{?fedora} >= 24 || 0%{?rhel} >= 7 || 0%{?suse_version} >= 1315
%{!?sfcgal:%global     sfcgal 1}
%else
%{!?sfcgal:%global    sfcgal 0}
%endif

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	Geographic Information Systems Extensions to PostgreSQL
Name:		%{sname}%{postgiscurrmajorversion}_%{pg_dotless}
Version:	%{rpmbuild_version}
Release:	%{rpmbuild_release}%{?dist}
License:	GPLv2+
Group:		Applications/Databases
Source0:	https://download.osgeo.org/postgis/source/postgis-%{version}.tar.gz
Source2:	https://download.osgeo.org/postgis/docs/postgis-%{version}.pdf
Source4:	postgis-filter-requires-perl-Pg.sh
Patch0:		postgis-gdalfpic.patch

URL:		http://www.postgis.net/

BuildRequires:	postgresql%{pg_dotless}-devel, geos36-devel >= 3.6.2, pcre-devel
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:  libjson-c-devel libproj-devel
%endif
%else
BuildRequires:	proj49-devel, flex, json-c-devel
%endif
BuildRequires:	libxml2-devel
%if %{sfcgal}
BuildRequires:	SFCGAL-devel
Requires:	SFCGAL
%endif
%if %{raster}
BuildRequires:	gdal-devel >= 1.9.0
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

Requires:	postgresql%{pg_dotless} geos36 >= 3.6.2
Requires:	postgresql%{pg_dotless}-contrib proj49
%if 0%{?rhel} && 0%{?rhel} < 6
Requires:	hdf5 < 1.8.7
%else
Requires:	hdf5
%endif

Requires:	pcre
%if 0%{?suse_version} >= 1315
Requires:	libjson-c2 libgdal20
%else
Requires:	json-c gdal-libs >= 1.9.0
%endif
Requires(post):	%{_sbindir}/update-alternatives

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

Provides:	%{sname} = %{version}-%{release}
Obsoletes:	%{sname}2_%{pg_dotless} <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pg_dotless} => %{postgismajorversion}.0

%description
PostGIS adds support for geographic objects to the PostgreSQL object-relational
database. In effect, PostGIS "spatially enables" the PostgreSQL server,
allowing it to be used as a backend spatial database for geographic information
systems (GIS), much like ESRI's SDE or Oracle's Spatial extension. PostGIS
follows the OpenGIS "Simple Features Specification for SQL" and has been
certified as compliant with the "Types and Functions" profile.

%package client
Summary:	Client tools and their libraries of PostGIS
Group:		Applications/Databases
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:	%{sname}-client = %{version}-%{release}
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif
Obsoletes:	%{sname}2_%{pg_dotless}-client <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pg_dotless}-client => %{postgismajorversion}.0

%description client
The %{name}-client package contains the client tools and their libraries
of PostGIS.

%package devel
Summary:	Development headers and libraries for PostGIS
Group:		Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:	%{sname}-devel = %{version}-%{release}
Obsoletes:	%{sname}2_%{pg_dotless}-devel <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pg_dotless}-devel => %{postgismajorversion}.0
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description devel
The %{name}-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with PostGIS.

%package docs
Summary:	Extra documentation for PostGIS
Group:		Applications/Databases
Obsoletes:	%{sname}2_%{pg_dotless}-docs <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pg_dotless}-docs => %{postgismajorversion}.0
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description docs
The %{name}-docs package includes PDF documentation of PostGIS.

%if %utils
%package utils
Summary:	The utils for PostGIS
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release}, perl-DBD-Pg
Provides:	%{sname}-utils = %{version}-%{release}
Obsoletes:	%{sname}2_%{pg_dotless}-utils <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pg_dotless}-utils => %{postgismajorversion}.0
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description utils
The %{name}-utils package provides the utilities for PostGIS.
%endif

%global __perl_requires %{SOURCE4}

%prep
%setup -q -n %{sname}-%{version}
# Copy .pdf file to top directory before installing.
%{__cp} -p %{SOURCE2} .
%patch0 -p0
# Patch1 can be removed when 2.4.6 comes out
%patch1 -p0

%build

%ifarch ppc64 ppc64le
        sed -i 's:^GEOS_LDFLAGS=:GEOS_LDFLAGS=-L%{atpath}/%{_lib} :g' configure
        CFLAGS="-O3 -mcpu=power8 -mtune=power8 -I%{atpath}/include" LDFLAGS="-L%{atpath}/%{_lib}"
        sed -i 's:^LDFLAGS = :LDFLAGS = -L%{atpath}/%{_lib} :g' raster/loader/Makefile.in
	CC=%{atpath}/bin/gcc; export CC
%endif

LDFLAGS="$LDFLAGS -L/usr/geos36/lib -L/usr/proj49/lib"; export LDFLAGS

%configure --with-pgconfig=%{pginstdir}/bin/pg_config \
%if !%raster
        --without-raster \
%endif
%if %{sfcgal}
	--with-sfcgal=%{_bindir}/sfcgal-config \
%endif
%if %{shp2pgsqlgui}
	--with-gui \
%endif
	--disable-rpath --libdir=%{pginstdir}/lib \
	--with-geosconfig=/usr/geos36/bin/geos-config \
	--with-projdir=/usr/proj49

%{__make} LPATH=`%{pginstdir}/bin/pg_config --pkglibdir` shlib="%{name}.so"
%{__make} -C extensions

%if %utils
 %{__make} -C utils
%endif

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%if %utils
install -d %{buildroot}%{_datadir}/%{name}
install -m 644 utils/*.pl %{buildroot}%{_datadir}/%{name}
%endif

# Create symlink of .so file. PostGIS hackers said that this is safe:
%{__ln_s} %{pginstdir}/lib/%{sname}-%{postgismajorversion}.so %{buildroot}%{pginstdir}/lib/%{sname}-%{postgisprevmajorversion}.so

# Create alternatives entries for common binaries
%post
%{_sbindir}/update-alternatives --install /usr/bin/pgsql2shp postgis-pgsql2shp %{pginstdir}/bin/pgsql2shp %{pg_dotless}0
%{_sbindir}/update-alternatives --install /usr/bin/shp2pgsql postgis-shp2pgsql %{pginstdir}/bin/shp2pgsql %{pg_dotless}0

# Drop alternatives entries for common binaries and man files
%postun
if [ "$1" -eq 0 ]
  then
      	# Only remove these links if the package is completely removed from the system (vs.just being upgraded)
        %{_sbindir}/update-alternatives --remove postgis-pgsql2shp	%{pginstdir}/bin/pgsql2shp
        %{_sbindir}/update-alternatives --remove postgis-shp2pgsql	%{pginstdir}/bin/shp2pgsql
fi

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING CREDITS NEWS TODO README.%{sname} doc/html loader/README.* doc/%{sname}.xml doc/ZMSgeoms.txt
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE.TXT
%else
%license LICENSE.TXT
%endif
%{pginstdir}/doc/extension/README.address_standardizer
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_comments.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_for_extension.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_upgrade*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_restore.pl
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_postgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/legacy*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/*topology*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_proc_set_search_path.sql
%if %{sfcgal}
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/*sfcgal*.sql
%endif
%{pginstdir}/lib/%{sname}-%{postgisprevmajorversion}.so
%attr(755,root,root) %{pginstdir}/lib/%{sname}-%{postgismajorversion}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%if %{sfcgal}
%{pginstdir}/share/extension/%{sname}_sfcgal*.sql
%{pginstdir}/share/extension/%{sname}_sfcgal.control
%endif
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/lib/liblwgeom*.so.*
%{pginstdir}/lib/postgis_topology-%{postgismajorversion}.so
%{pginstdir}/lib/address_standardizer-%{postgismajorversion}.so
%{pginstdir}/lib/liblwgeom.so
%{pginstdir}/share/extension/address_standardizer*.sql
%{pginstdir}/share/extension/address_standardizer*.control
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/sfcgal_comments.sql
%if %raster
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/raster_comments.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/*rtpostgis*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_legacy.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/spatial*.sql
%{pginstdir}/lib/rtpostgis-%{postgismajorversion}.so
%{pginstdir}/share/extension/%{sname}_topology-*.sql
%{pginstdir}/share/extension/%{sname}_topology.control
%{pginstdir}/share/extension/%{sname}_tiger_geocoder*.sql
%{pginstdir}/share/extension/%{sname}_tiger_geocoder.control
%ifarch ppc64 ppc64le
 %else
 %if %{pg_dotless} >= 11 && %{pg_dotless} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/address_standardizer-%{postgismajorversion}*.bc
   %{pginstdir}/lib/bitcode/address_standardizer-%{postgismajorversion}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}_topology-%{postgismajorversion}*.bc
   %{pginstdir}/lib/bitcode/%{sname}_topology-%{postgismajorversion}/*.bc
   %{pginstdir}/lib/bitcode/rt%{sname}-%{postgismajorversion}*.bc
   %{pginstdir}/lib/bitcode/rt%{sname}-%{postgismajorversion}/*.bc
  %endif
 %endif
%endif
%endif

%files client
%defattr(644,root,root)
%attr(755,root,root) %{pginstdir}/bin/pgsql2shp
%attr(755,root,root) %{pginstdir}/bin/raster2pgsql
%attr(755,root,root) %{pginstdir}/bin/shp2pgsql

%files devel
%defattr(644,root,root)
%{_includedir}/liblwgeom.h
%{_includedir}/liblwgeom_topo.h
%{pginstdir}/lib/liblwgeom*.a
%{pginstdir}/lib/liblwgeom*.la

%if %utils
%files utils
%defattr(-,root,root)
%doc utils/README
%attr(755,root,root) %{_datadir}/%{name}/*.pl
%endif

%files docs
%defattr(-,root,root)
%doc %{sname}-%{version}.pdf

%changelog
* Mon Sep 24 2018 Justin Bronn <justin.bronn@radiantsolutions.com> - 2.4.4-1
- Initial release, version 2.4.4.
