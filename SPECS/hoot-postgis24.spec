%global postgismajorversion 2.4
%global postgiscurrmajorversion %(echo %{postgismajorversion}|tr -d '.')
%global postgisprevmajorversion 2.3
%global sname	postgis

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
%ifnarch ppc64 ppc64le
%{!?sfcgal:%global     sfcgal 1}
%else
%{!?sfcgal:%global     sfcgal 0}
%endif
%else
%{!?sfcgal:%global    sfcgal 0}
%endif

%ifarch ppc64 ppc64le
# Define the AT version and path.
%global atstring	at10.0
%global atpath		/opt/%{atstring}
%endif

Summary:	Geographic Information Systems Extensions to PostgreSQL
Name:		%{sname}%{postgiscurrmajorversion}_%{pgmajorversion}
Version:	%{postgismajorversion}.5
Release:	1%{?dist}
License:	GPLv2+
Group:		Applications/Databases
Source0:	https://download.osgeo.org/%{sname}/source/%{sname}-%{version}.tar.gz
Source2:	https://download.osgeo.org/%{sname}/docs/%{sname}-%{version}.pdf
Source4:	%{sname}%{postgiscurrmajorversion}-filter-requires-perl-Pg.sh
Patch0:		%{sname}%{postgiscurrmajorversion}-%{postgismajorversion}.0-gdalfpic.patch
# Patch1 can be removed when 2.4.6 comes out
Patch1:		%{sname}%{postgiscurrmajorversion}-%{postgismajorversion}.5-clangfix.patch

URL:		http://www.postgis.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql%{pgmajorversion}-devel, geos36-devel >= 3.6.2, pcre-devel
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:  libjson-c-devel libproj-devel
%endif
%else
BuildRequires:	proj49-devel, flex, json-c-devel
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
BuildRequires:	gdal-devel >= 1.9.0
%endif

%ifarch ppc64 ppc64le
BuildRequires:	advance-toolchain-%{atstring}-devel
%endif

Requires:	postgresql%{pgmajorversion} geos36 >= 3.6.2
Requires:	postgresql%{pgmajorversion}-contrib proj49
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
Obsoletes:	%{sname}2_%{pgmajorversion} <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pgmajorversion} => %{postgismajorversion}.0

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
Obsoletes:	%{sname}2_%{pgmajorversion}-client <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pgmajorversion}-client => %{postgismajorversion}.0

%description client
The %{name}-client package contains the client tools and their libraries
of PostGIS.

%package devel
Summary:	Development headers and libraries for PostGIS
Group:		Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:	%{sname}-devel = %{version}-%{release}
Obsoletes:	%{sname}2_%{pgmajorversion}-devel <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pgmajorversion}-devel => %{postgismajorversion}.0
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
Obsoletes:	%{sname}2_%{pgmajorversion}-docs <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pgmajorversion}-docs => %{postgismajorversion}.0
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
Obsoletes:	%{sname}2_%{pgmajorversion}-utils <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pgmajorversion}-utils => %{postgismajorversion}.0
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
%{_sbindir}/update-alternatives --install /usr/bin/pgsql2shp postgis-pgsql2shp %{pginstdir}/bin/pgsql2shp %{pgmajorversion}0
%{_sbindir}/update-alternatives --install /usr/bin/shp2pgsql postgis-shp2pgsql %{pginstdir}/bin/shp2pgsql %{pgmajorversion}0

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
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
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
%if %shp2pgsqlgui
%{pginstdir}/bin/shp2pgsql-gui
%{pginstdir}/share/applications/shp2pgsql-gui.desktop
%{pginstdir}/share/icons/hicolor/*/apps/shp2pgsql-gui.png
%endif
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}-%{postgismajorversion}*.bc
   %{pginstdir}/lib/bitcode/%{sname}-%{postgismajorversion}/*.bc
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
* Tue Sep 18 2018 John K. Harvey <john.harvey@crunchydata.com> - 2.4.5-1
- Update to 2.4.5
- Includes patchfile to support 2.4.5 working with clang on PG11 for EL-7

* Thu May 3 2018 Devrim Gündüz <devrim@gunduz.org> - 2.4.4-2
- Remove 2.3 bits from the package, and use symlink to .so file
  instead.

* Tue Apr 10 2018 Devrim Gündüz <devrim@gunduz.org> - 2.4.4-1
- Update to 2.4.4

* Thu Jan 18 2018 Devrim Gündüz <devrim@gunduz.org> - 2.4.3-1
- Update to 2.4.3, per #3022.
- Update previous PostGIS version to 2.3.6.

* Mon Dec 25 2017 Devrim Gündüz <devrim@gunduz.org> - 2.4.2-5
- Rebuilt

* Tue Dec 19 2017 Devrim Gündüz <devrim@gunduz.org> - 2.4.2-4
- Rebuilt

* Thu Nov 23 2017 Devrim Gündüz <devrim@gunduz.org> - 2.4.2-3
- Make sure that we link against our GeOS and Proj packages.

* Wed Nov 22 2017 Devrim Gündüz <devrim@gunduz.org> - 2.4.2-2
- Let PostGIS depend on PGDG supplied Proj49 and GeOS 36 RPMs.
  This will help users to benefit from latest GeOS and Proj.

* Thu Nov 16 2017 Devrim Gündüz <devrim@gunduz.org> - 2.4.2-1
- Update to 2.4.2, per #2874.
- Update previous PostGIS version to 2.3.5.

* Sat Oct 21 2017 Devrim Gündüz <devrim@gunduz.org> - 2.4.1-1
- Update to 2.4.1, per #2819.
- Re-add 2.3 .so file for easier upgrades (2.3 can be compiled
  against PostgreSQL 10 as of 2.3.4)

* Wed Oct 18 2017 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-2
- Require postgresql-contrib for postgis_tiger_geocoder,
  because it requires fuzzystrmatch extension.

* Fri Sep 29 2017 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-1
- Update to 2.4.0

* Wed Sep 27 2017 Devrim Gündüz <devrim@gunduz.org> - 2.4.0rc3-1
- Initial packaging for 2.4

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
