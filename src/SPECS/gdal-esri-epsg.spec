####
### This is far from complete. Just playing.
####
Name:		gdal-esri-epsg
Version:	1.10.1
Release:	1%{?dist}
Summary:	GIS file format support files

Group:		System Environment/Libraries
License:	Unknown
URL:		http://www.gdal.org

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       gdal >= %{version}
#Source0:        http://download.osgeo.org/gdal/%{version}/gdal-%{version}.tar.gz
Source0:        gdal-%{version}.tar.gz

%description
The license for the EPSG codes distributed with GDAL are a bit complicated. See:
https://trac.osgeo.org/gdal/wiki/RevisedEPSGLicense

As a result they aren't included in the standard GDAL RPM.

%files
/usr/share/gdal/cubewerx_extra.wkt
/usr/share/gdal/esri_extra.wkt
/usr/share/gdal/esri_Wisconsin_extra.wkt
/usr/share/gdal/esri_StatePlane_extra.wkt
/usr/share/gdal/ecw_cs.wkt

%prep
mkdir -p %{name}-%{version}
cd %{name}-%{version}
tar xf %{_sourcedir}/gdal-%{version}.tar.gz
cd gdal-%{version}

%build
true

%install
export DATA_DIR=$RPM_BUILD_DIR/$RPM_PACKAGE_NAME-$RPM_PACKAGE_VERSION/gdal-$RPM_PACKAGE_VERSION/data
export INSTALL_DIR=$RPM_BUILD_ROOT/usr/share/gdal/
mkdir -p $INSTALL_DIR

install $DATA_DIR/cubewerx_extra.wkt $INSTALL_DIR
install $DATA_DIR/esri_extra.wkt $INSTALL_DIR
install $DATA_DIR/esri_Wisconsin_extra.wkt $INSTALL_DIR
install $DATA_DIR/esri_StatePlane_extra.wkt $INSTALL_DIR
install $DATA_DIR/ecw_cs.wkt $INSTALL_DIR

%check

%clean
#rm -rf %{buildroot}

%changelog
* Thu Jan 25 2016 Jason R. Surratt <jason.surratt@digitalglobe.com> - 0.2.21+
- Initial attempt
