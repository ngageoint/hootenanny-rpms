Name:		hootenanny
Version:	0.2.20_204_gfc1455e_dirty
Release:	1%{?dist}
Summary:	Hootenanny is a vector conflation suite.

Group:		Applications/Engineering
License:	GPLv3
URL:		https://github.com/ngageoint/hootenanny

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	git doxygen wget w3m words automake gcc
Source0:        %{name}-%{version}.tar.gz

%description
Hootenanny was developed to provide an open source, standards-based approach to
geospatial vector data conflation. Hootenanny is designed to facilitate
automated and semi-automated conflation of critical foundation GEOINT features
in the topographic domain, namely roads (polylines), buildings (polygons), and
points-of-interest (POI's) (points). Conflation happens at the dataset level,
where the user's workflow determines the best reference dataset and source
content, geometry and attributes, to transfer to the output map.

%package core
Summary:	Hootenanny Core
Requires:       %{name}-core-deps
Group:		Applications/Engineering

%description core
Hootenanny was developed to provide an open source, standards-based approach to
geospatial vector data conflation. Hootenanny is designed to facilitate
automated and semi-automated conflation of critical foundation GEOINT features
in the topographic domain, namely roads (polylines), buildings (polygons), and
points-of-interest (POI's) (points). Conflation happens at the dataset level,
where the user's workflow determines the best reference dataset and source
content, geometry and attributes, to transfer to the output map.

This package contains the core algorithms and command line interface.

%prep
%setup -q -n %{name}-%{version}

%build
source ./SetupEnv.sh
./configure --with-rnd -q && make -s %{?_smp_mflags}

%install


%check
source ./SetupEnv.sh
HootTest --slow

%clean
rm -rf %{buildroot}

%files core

%package core-devel-deps
Summary:	Development dependencies for Hootenanny Core
Group:		Development/Libraries
Requires:	%{name}-core-deps = %{version}-%{release}
Requires:	autoconf automake boost-devel cppunit-devel gcc-c++
Requires:       gdal-devel >= 1.10.1
Requires:       gdb
Requires:       geos-devel = 3.4.2
Requires:       git glpk-devel libicu-devel nodejs-devel opencv-devel
Requires:       postgresql91-devel proj-devel protobuf-devel python-argparse python-devel qt-devel v8-devel

%description core-devel-deps
Hootenanny was developed to provide an open source, standards-based approach to
geospatial vector data conflation. Hootenanny is designed to facilitate
automated and semi-automated conflation of critical foundation GEOINT features
in the topographic domain, namely roads (polylines), buildings (polygons), and
points-of-interest (POI's) (points). Conflation happens at the dataset level,
where the user's workflow determines the best reference dataset and source
content, geometry and attributes, to transfer to the output map.

This packages contains the dependencies to build and develop the Hootenanny
core. Use this if you want to build from github.

%files core-devel-deps

%package core-deps
Summary:	Dependencies for Hootenanny Core
Group:		Development/Libraries
Requires:	asciidoc cppunit dblatex doxygen FileGDB_API
Requires:       gdal >= 1.10.1
Requires: 	gdal-esri-epsg >= 1.10.1
Requires:       geos = 3.4.2, gnuplot, graphviz
# Needed by gnuplot
Requires:       liberation-fonts-common liberation-sans-fonts
Requires:       libxslt nodejs opencv postgresql91-libs protobuf qt
Requires:       texlive texlive-collection-langcyrillic
Requires:       unzip w3m wget words
Requires:       zip

%description core-deps
Hootenanny was developed to provide an open source, standards-based approach to
geospatial vector data conflation. Hootenanny is designed to facilitate
automated and semi-automated conflation of critical foundation GEOINT features
in the topographic domain, namely roads (polylines), buildings (polygons), and
points-of-interest (POI's) (points). Conflation happens at the dataset level,
where the user's workflow determines the best reference dataset and source
content, geometry and attributes, to transfer to the output map.

This packages contains the dependencies to run the Hootenanny core.

%files core-deps

%changelog
* Thu Jan 21 2016 Jason R. Surratt <jason.surratt@digitalglobe.com> - 0.2.21+
- Initial attempt
