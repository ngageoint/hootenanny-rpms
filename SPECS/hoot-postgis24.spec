%global postgis_major %(echo %{rpmbuild_version} | awk -F. '{ print $1 }')
%global postgis_minor %(echo %{rpmbuild_version} | awk -F. '{ print $2 }')
%global postgis_micro %(echo %{rpmbuild_version} | awk -F. '{ print $3 }')
%global postgismajorversion %{postgis_major}.%{postgis_minor}
%global postgiscurrmajorversion %(echo %{postgismajorversion}|tr -d '.')
%global postgisprevmajorversion 2.3
%global postgisprev_dotless %(echo %{postgisprevmajorversion}|tr -d '.')
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

BuildRequires:  postgresql%{pg_dotless}-devel
BuildRequires:  geos-devel >= 3.6.2
BuildRequires:  pcre-devel
BuildRequires:  proj-devel
BuildRequires:  flex
BuildRequires:  json-c-devel
BuildRequires:  libxml2-devel
%if %{sfcgal}
BuildRequires:	SFCGAL-devel
Requires:	SFCGAL
%endif
%if %{raster}
BuildRequires:	hoot-gdal-devel >= 2.1.0
%endif

Requires:	geos >= 3.6.2
Requires:	hdf5
Requires:	hoot-gdal-libs >= 2.1.0
Requires:	json-c
Requires:	postgresql%{pg_dotless}
Requires:	postgresql%{pg_dotless}-contrib
Requires:	proj
Requires:	pcre
Requires(post):	%{_sbindir}/update-alternatives

Obsoletes:	%{sname}%{postgisprev_dotless}_%{pg_dotless}
Provides:	%{sname}%{pg_dotless} = %{version}-%{release}
Provides:	%{sname}%{postgisprev_dotless}_%{pg_dotless} = %{version}-%{release}
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
Obsoletes:	%{sname}%{postgisprev_dotless}_%{pg_dotless}-client
Provides:	%{sname}%{pg_dotless}-client = %{version}-%{release}
Provides:	%{sname}%{postgisprev_dotless}_%{pg_dotless}-client = %{version}-%{release}
Conflicts:	postgis-client
Conflicts:	postgis%{postgiscurrmajorversion}_%{pg_dotless}-client

%description client
The %{name}-client package contains the client tools and their libraries
of PostGIS.

%package devel
Summary:	Development headers and libraries for PostGIS
Group:		Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:	%{sname}%{postgisprev_dotless}_%{pg_dotless}-devel
Provides:	%{sname}%{pg_dotless}-devel = %{version}-%{release}
Provides:	%{sname}%{postgisprev_dotless}_%{pg_dotless}-devel = %{version}-%{release}
Conflicts:	postgis-devel
Conflicts:	postgis%{postgiscurrmajorversion}_%{pg_dotless}-devel

%description devel
The %{name}-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with PostGIS.

%package docs
Summary:	Extra documentation for PostGIS
Group:		Applications/Databases
Obsoletes:	%{sname}%{postgisprev_dotless}_%{pg_dotless}-docs
Provides:	%{sname}%{pg_dotless}-docs = %{version}-%{release}
Provides:	%{sname}%{postgisprev_dotless}_%{pg_dotless}-docs = %{version}-%{release}
Conflicts:	postgis-docs
Conflicts:	postgis%{postgiscurrmajorversion}_%{pg_dotless}-docs

%description docs
The %{name}-docs package includes PDF documentation of PostGIS.

%if %utils
%package utils
Summary:	The utils for PostGIS
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release}
Requires:	perl-DBD-Pg
Obsoletes:	%{sname}%{postgisprev_dotless}_%{pg_dotless}-utils
Provides:	%{sname}%{pg_dotless}-utils = %{version}-%{release}
Provides:	%{sname}%{postgisprev_dotless}_%{pg_dotless}-utils = %{version}-%{release}
Conflicts:	postgis-utils
Conflicts:	postgis%{postgiscurrmajorversion}_%{pg_dotless}-utils

%description utils
The %{name}-utils package provides the utilities for PostGIS.
%endif

%global __perl_requires %{SOURCE4}

%prep
%setup -q -n postgis-%{version}
# Copy .pdf file to top directory before installing.
%{__cp} -p %{SOURCE2} .
%patch0 -p0

%build

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
%{__install} -d %{buildroot}%{_datadir}/%{name}
%{__install} -m 0644 utils/*.pl %{buildroot}%{_datadir}/%{name}
%endif

# Create symlink of .so file. PostGIS hackers said that this is safe:
%{__ln_s} %{pginstdir}/lib/postgis-%{postgismajorversion}.so %{buildroot}%{pginstdir}/lib/postgis-%{postgisprevmajorversion}.so

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
%{pginstdir}/lib/postgis-%{postgisprevmajorversion}.so
%attr(0755,root,root) %{pginstdir}/lib/postgis-%{postgismajorversion}.so
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
%defattr(0644,root,root)
%attr(0755,root,root) %{pginstdir}/bin/pgsql2shp
%attr(0755,root,root) %{pginstdir}/bin/raster2pgsql
%attr(0755,root,root) %{pginstdir}/bin/shp2pgsql

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
%attr(0755,root,root) %{_datadir}/%{name}/*.pl
%endif

%files docs
%defattr(-,root,root)
%doc postgis-%{version}.pdf

%changelog
* Fri Oct 05 2018 Justin Bronn <justin.bronn@radiantsolutions.com> - 2.4.4-2
- Fix packaging issues in initial release.

* Mon Sep 24 2018 Justin Bronn <justin.bronn@radiantsolutions.com> - 2.4.4-1
- Initial release, version 2.4.4.
