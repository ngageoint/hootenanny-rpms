%global postgismajorversion 2.3
%global postgiscurrmajorversion %(echo %{postgismajorversion}|tr -d '.')
%global postgisprevmajorversion 2.2
%global postgisprevversion %{postgisprevmajorversion}.6
%global sname hoot-postgis

%{!?utils:%global	utils 1}
%if 0%{?fedora} >= 24 || 0%{?rhel} >= 7 || 0%{?suse_version} >= 1315
%{!?shp2pgsqlgui:%global	shp2pgsqlgui 1}
%else
%{!?shp2pgsqlgui:%global	shp2pgsqlgui 0}
%endif
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
Version:	%{postgismajorversion}.4
Release:	1%{?dist}
License:	GPLv2+
Group:		Applications/Databases
Source0:	http://download.osgeo.org/postgis/source/postgis-%{version}.tar.gz
Source1:	http://download.osgeo.org/postgis/source/postgis-%{postgisprevversion}.tar.gz
Source2:	http://download.osgeo.org/postgis/docs/postgis-%{version}.pdf
Source4:	postgis-filter-requires-perl-Pg.sh
Patch0:		postgis-gdalfpic.patch

URL:		http://www.postgis.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql%{pg_dotless}-devel, geos-devel >= 3.5.0, pcre-devel
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:  libjson-c-devel libproj-devel
%endif
%else
BuildRequires:	proj-devel, flex, json-c-devel
%endif
BuildRequires:	libxml2-devel
%if %{shp2pgsqlgui}
BuildRequires:	gtk2-devel > 2.8.0
%endif
%if %{sfcgal}
BuildRequires:	SFCGAL-devel
Requires:	SFCGAL
%endif
%if %{raster}
BuildRequires:	hoot-gdal-devel >= 2.1.0
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

Requires:	postgresql%{pg_dotless}, geos >= 3.5.0, proj
%if 0%{?rhel} && 0%{?rhel} < 6
Requires:	hdf5 < 1.8.7
%else
Requires:	hdf5
%endif

Requires:	hoot-gdal-libs > 2.1.0, json-c, pcre
Requires(post):	%{_sbindir}/update-alternatives

%ifarch ppc64 ppc64le
AutoReq:	0
Requires:	advance-toolchain-%{atstring}-runtime
%endif

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
%if %{shp2pgsqlgui}
	--with-gui \
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
%if %shp2pgsqlgui
%{pginstdir}/bin/shp2pgsql-gui
%{pginstdir}/share/applications/shp2pgsql-gui.desktop
%{pginstdir}/share/icons/hicolor/*/apps/shp2pgsql-gui.png
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
* Sun Jul 2 2017 Devrim Gündüz <devrim@gunduz.org> - 2.3.3-1
- Update to 2.3.3, per #2525 .

* Sun May 28 2017 Devrim Gündüz <devrim@gunduz.org> - 2.3.2-2
- Rename package so that it also includes the Postgis major version.

* Mon Nov 28 2016 Devrim Gündüz <devrim@gunduz.org> - 2.3.2-1
- Update to 2.3.2, per changes described at
  http://postgis.net/2017/01/31/postgis-2.3.2
- Update previous PostGIS version to 2.2.5, per changes described at
  http://postgis.net/2017/01/30/postgis-2.2.5

* Mon Nov 28 2016 Devrim Gündüz <devrim@gunduz.org> - 2.3.1-1
- Update to 2.3.1, per changes described at
  http://postgis.net/2016/11/28/postgis-2.3.1/
- Update previous PostGIS version to 2.2.4

* Thu Oct 6 2016 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-3
- Update previous PostGIS version to 2.2.3
- Update comments about the previous version to point to the
  new releases.

* Sat Oct 01 2016 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-2
- Rebuilt for new gdal

* Wed Sep 28 2016 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-1
- Update to 2.3.0, per changes described at
  http://postgis.net/2016/09/26/postgis-2.3.0/
- Remove wildcard in -client subpackage, per John. Fixes #1769.

* Fri Mar 25 2016 Devrim Gündüz <devrim@gunduz.org> - 2.2.2-1
- Update to 2.2.2, per changes described at
  http://postgis.net/2016/03/22/postgis-2.2.2
- Do not attempt to install some files twice.
- Support --with-gui configure option. Patch from John Harvey,
  per #1036.

* Mon Feb 22 2016 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-3
- Fix GeOS version number in Requires part, so that it *also*
  requires GeOS >= 3.5.0. Per #1007.
- Add dependency for pcre, per #1007.

* Mon Jan 18 2016 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-3
- Force dependency on GeOS 3.5.0. Per report from Paul Edwards,
  and others, on PostGIS mailing list.

* Mon Jan 11 2016 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-2
- Fix utils, and raster macros, to fix builds on RHEL 6.
- Add macro for sfcgal support.

* Wed Jan 06 2016 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-1
- Update to 2.2.1, per changes described at:
  http://postgis.net/2016/01/06/postgis-2.2.1/
- Use %%license macro, on supported distros.
- Put sfcgal and raster support into conditionals, so that
  we can use one spec file for all platforms.

* Fri Oct 30 2015 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.2.0-2
- Build with SFCGAL support.
- use -fPIC with gdal, patch from Oskari Saarenmaa.

* Tue Oct 13 2015 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.2.0-1
- Update to 2.2.0, per changes described at:
  http://postgis.net/2015/10/07/postgis-2.2.0
  using 2.1.8 spec file.
- Don't use smp_flags in make, as it breaks build.
- Trim changelog.
