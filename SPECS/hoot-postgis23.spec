%global postgis_major %(echo %{rpmbuild_version} | awk -F. '{ print $1 }')
%global postgis_minor %(echo %{rpmbuild_version} | awk -F. '{ print $2 }')
%global postgis_micro %(echo %{rpmbuild_version} | awk -F. '{ print $3 }')
%global postgismajorversion %{postgis_major}.%{postgis_minor}
%global postgiscurrmajorversion %(echo %{postgismajorversion}|tr -d '.')
%global postgisprevmajorversion 2.2
%global postgisprevversion %{postgisprevmajorversion}.6
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
Source0:	http://download.osgeo.org/postgis/source/postgis-%{version}.tar.gz
Source1:	http://download.osgeo.org/postgis/source/postgis-%{postgisprevversion}.tar.gz
Source2:	http://download.osgeo.org/postgis/docs/postgis-%{version}.pdf
Source4:	postgis-filter-requires-perl-Pg.sh
Patch0:		postgis-gdalfpic.patch

URL:		http://www.postgis.net/

BuildRequires:	postgresql%{pg_dotless}-devel
BuildRequires:	geos-devel >= 3.5.0
BuildRequires:	pcre-devel
BuildRequires:	proj-devel
BuildRequires:	flex
BuildRequires:	json-c-devel
BuildRequires:	libxml2-devel
%if %{sfcgal}
BuildRequires:	SFCGAL-devel
Requires:	SFCGAL
%endif
%if %{raster}
BuildRequires:	hoot-gdal-devel >= 2.1.0
%endif

# %ifarch ppc64 ppc64le
# BuildRequires:	advance-toolchain-%{atstring}-devel
# %endif

Requires:	postgresql%{pg_dotless}, geos >= 3.5.0, proj
%if 0%{?rhel} && 0%{?rhel} < 6
Requires:	hdf5 < 1.8.7
%else
Requires:	hdf5
%endif

Requires:	hoot-gdal-libs > 2.1.0, json-c, pcre
Requires(post):	%{_sbindir}/update-alternatives

# %ifarch ppc64 ppc64le
# AutoReq:	0
# Requires:	advance-toolchain-%{atstring}-runtime
# %endif

Provides:	%{sname} = %{version}-%{release}
Conflicts:	postgis
Conflicts:	postgis%{postgiscurrmajorversion}_%{pg_dotless}

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
Conflicts:	postgis-client
Conflicts:	postgis%{postgiscurrmajorversion}_%{pg_dotless}-client
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description client
The postgis-client package contains the client tools and their libraries
of PostGIS.

%package devel
Summary:	Development headers and libraries for PostGIS
Group:		Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:	%{sname}-devel = %{version}-%{release}
Conflicts:	postgis-devel
Conflicts:	postgis%{postgiscurrmajorversion}_%{pg_dotless}-devel
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description devel
The postgis-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with PostGIS.

%package docs
Summary:	Extra documentation for PostGIS
Group:		Applications/Databases
Conflicts:	postgis-docs
Conflicts:	postgis%{postgiscurrmajorversion}_%{pg_dotless}-docs

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description docs
The postgis-docs package includes PDF documentation of PostGIS.

%if %utils
%package utils
Summary:	The utils for PostGIS
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release}, perl-DBD-Pg
Provides:	%{sname}-utils = %{version}-%{release}
Conflicts:	postgis-utils
Conflicts:	postgis%{postgiscurrmajorversion}_%{pg_dotless}-utils
%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

%description utils
The postgis-utils package provides the utilities for PostGIS.
%endif

%global __perl_requires %{SOURCE4}

%prep
%setup -q -n postgis-%{version}
# Copy .pdf file to top directory before installing.
%{__cp} -p %{SOURCE2} .
%patch0 -p0

%build

%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif

%configure --with-pgconfig=%{pginstdir}/bin/pg_config \
%if !%raster
        --without-raster \
%endif
%if %{sfcgal}
	--with-sfcgal=%{_bindir}/sfcgal-config \
%endif
	--disable-rpath --libdir=%{pginstdir}/lib

%{__make} LPATH=`%{pginstdir}/bin/pg_config --pkglibdir` shlib="%{name}.so"
%{__make} -C extensions

%if %utils
 %{__make} -C utils
%endif

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%if %utils
install -d %{buildroot}%{_datadir}/postgis%{postgiscurrmajorversion}_%{pg_dotless}
install -m 0644 utils/*.pl %{buildroot}%{_datadir}/postgis%{postgiscurrmajorversion}_%{pg_dotless}
%endif

# PostGIS 2.3 breaks compatibility with 2.2, and we need to ship
# postgis-2.2.so file along with 2.2 package, so that we can upgrade:
tar zxf %{SOURCE1}
cd postgis-%{postgisprevversion}
%ifarch ppc64 ppc64le
	CFLAGS="${CFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	CXXFLAGS="${CXXFLAGS} $(echo %{__global_cflags} | sed 's/-O2/-O3/g') -m64 -mcpu=power8 -mtune=power8 -I%{atpath}/include"
	LDFLAGS="-L%{atpath}/%{_lib}"
	CC=%{atpath}/bin/gcc; export CC
%endif

%configure --with-pgconfig=%{pginstdir}/bin/pg_config --without-raster \
	 --disable-rpath --libdir=%{pginstdir}/lib

%{__make} LPATH=`%{pginstdir}/bin/pg_config --pkglibdir` shlib="postgis-%{postgisprevmajorversion}.so"
# Install postgis-2.2.so file manually:
%{__mkdir} -p %{buildroot}/%{pginstdir}/lib/
%{__install} -m 0644 postgis/postgis-%{postgisprevmajorversion}.so %{buildroot}/%{pginstdir}/lib/postgis-%{postgisprevmajorversion}.so

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
%doc COPYING CREDITS NEWS TODO README.postgis doc/html loader/README.* doc/postgis.xml doc/ZMSgeoms.txt
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE.TXT
%else
%license LICENSE.TXT
%endif
%{pginstdir}/doc/extension/README.address_standardizer
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/postgis.sql
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/postgis_comments.sql
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/postgis_for_extension.sql
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/postgis_upgrade*.sql
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/postgis_restore.pl
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/uninstall_postgis.sql
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/legacy*.sql
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/*topology*.sql
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/postgis_proc_set_search_path.sql
%if %{sfcgal}
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/*sfcgal*.sql
%endif
%attr(755,root,root) %{pginstdir}/lib/postgis-%{postgisprevmajorversion}.so
%attr(755,root,root) %{pginstdir}/lib/postgis-%{postgismajorversion}.so
%{pginstdir}/share/extension/postgis-*.sql
%if %{sfcgal}
%{pginstdir}/share/extension/postgis_sfcgal*.sql
%{pginstdir}/share/extension/postgis_sfcgal.control
%endif
%{pginstdir}/share/extension/postgis.control
%{pginstdir}/lib/liblwgeom*.so.*
%{pginstdir}/lib/postgis_topology-%{postgismajorversion}.so
%{pginstdir}/lib/address_standardizer-%{postgismajorversion}.so
%{pginstdir}/lib/liblwgeom.so
%{pginstdir}/share/extension/address_standardizer*.sql
%{pginstdir}/share/extension/address_standardizer*.control
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/sfcgal_comments.sql
%if %raster
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/raster_comments.sql
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/*rtpostgis*.sql
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/uninstall_legacy.sql
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/spatial*.sql
%{pginstdir}/lib/rtpostgis-%{postgismajorversion}.so
%{pginstdir}/share/extension/postgis_topology-*.sql
%{pginstdir}/share/extension/postgis_topology.control
%{pginstdir}/share/extension/postgis_tiger_geocoder*.sql
%{pginstdir}/share/extension/postgis_tiger_geocoder.control
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
%attr(755,root,root) %{_datadir}/postgis%{postgiscurrmajorversion}_%{pg_dotless}/*.pl
%endif

%files docs
%defattr(-,root,root)
%doc postgis-%{version}.pdf

%changelog
* Wed Nov 29 2017 Justin Bronn <justin.bronn@digitalglobe.com> - 2.3.5-1
- Upgrade to 2.3.5.
* Wed Nov 15 2017 Justin Bronn <justin.bronn@digitalglobe.com> - 2.3.4-1
- Initial release.
