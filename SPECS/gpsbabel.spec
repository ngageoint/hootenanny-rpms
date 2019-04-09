Name:          gpsbabel
Version:       %{rpmbuild_version}
Release:       %{rpmbuild_release}%{?dist}
Summary:       A tool to convert between various formats used by GPS devices

License:       GPLv2+
URL:           http://www.gpsbabel.org
# Upstream's website hides tarball behind some ugly php script
# Original repo is at https://github.com/gpsbabel/gpsbabel
Source0:       %{name}-%{version}.tar.gz
Source2:       gpsbabel.png
Source21:      gpsbabel-style3.css
# Remove network access requirement for XML doc builds and HTML doc reading
Patch1:        gpsbabel-0001-1.4.2-xmldoc.patch
# Use system shapelib - not suitable for upstream in this form.
Patch2:        gpsbabel-0002-1.4.3-use-system-shapelib.patch
# Pickup gmapbase.html from /usr/share/gpsbabel
Patch3:        gpsbabel-0003-1.4.3-gmapbase.patch
# No automatic phone home by default (RHBZ 668865)
Patch4:        gpsbabel-0004-1.4.3-nosolicitation.patch
# Use system zlib
Patch5:        gpsbabel-0005-Use-system-zlib.patch
# Use system minizip
Patch6:        gpsbabel-0006-Use-system-minizip.patch
# Upstream patch
Patch7:        gpsbabel-0007-Added-geojson-read-capablity-moved-magic-strings.patch
# RHBZ#1561337
Patch8:        gpsbabel-0008-Correctly-read-diff-and-terr-from-geo-format.patch
# RHBZ#1625204
Patch9:        gpsbabel-0009-Remove-SHAPE-ZLIB-MINIZIP-from-LIBOBJS.patch


%global build_gui 1

BuildRequires: desktop-file-utils
BuildRequires: docbook-style-xsl
BuildRequires: expat-devel
BuildRequires: libusb-devel
BuildRequires: libxslt
BuildRequires: make
BuildRequires: minizip-devel
BuildRequires: perl
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtwebkit-devel
BuildRequires: qt5-linguist
BuildRequires: shapelib-devel
BuildRequires: zlib-devel


%description
Converts GPS waypoint, route, and track data from one format type
to another.

%if 0%{?build_gui}
%package gui
Summary:        Qt GUI interface for GPSBabel
License:        GPLv2+
Requires:       %{name} = %{version}-%{release}

%description gui
Qt GUI interface for GPSBabel
%endif

%prep
%setup -q -n %{name}-%{version}

# Use system shapelib instead of bundled partial shapelib
rm -rf shapelib

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

# FIXME: RHEL7 does not have qtwebengine
# Add define USE_GUI to switch between qtwebengine and qtwebkit
sed -i -e 's|greaterThan(QT_MINOR_VERSION, 5)|!equals(USE_GUI, "qtwebkit")|' gui/app.pro

# Get rid of bundled zlib
# configure --with-zlib=system is not enough,
# building still accesses bundled zlib headers
rm -rf zlib/*
touch zlib/empty.in

cp -p %{SOURCE21} gpsbabel.org-style3.css

# Avoid calling autoconf from Makefile
touch -r configure.in configure Makefile.in

%build
%configure --with-zlib=system --with-doc=./manual
%{__make} %{?_smp_mflags}
%{__perl} xmldoc/makedoc
%{__make} gpsbabel.html

%if 0%{?build_gui}
pushd gui
%{qmake_qt5} USE_GUI=qtwebkit
/usr/bin/lrelease-qt5 *.ts
%{__make} %{?_smp_mflags}
popd
%endif

%install
%{__make} DESTDIR=%{buildroot} install

%if 0%{?build_gui}
%{__make} -C gui DESTDIR=%{buildroot} install

install -m 0755 -d                            %{buildroot}%{_bindir}/
install -m 0755 -p gui/objects/gpsbabelfe-bin %{buildroot}%{_bindir}/
install -m 0755 -d                            %{buildroot}%{_qt5_translationdir}/
install -m 0644 -p gui/gpsbabel*_*.qm         %{buildroot}%{_qt5_translationdir}/

install -m 0755 -d %{buildroot}%{_datadir}/gpsbabel
install -m 0644 -p gui/gmapbase.html %{buildroot}%{_datadir}/gpsbabel

desktop-file-install \
        --dir %{buildroot}/%{_datadir}/applications \
        gui/gpsbabel.desktop

install -m 0755 -d            %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/
install -m 0644 -p %{SOURCE2} %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/

%find_lang %{name} --with-qt --all-name
%endif

%files
%doc README* AUTHORS
%license COPYING
%doc gpsbabel.html gpsbabel.org-style3.css
%{_bindir}/gpsbabel

%if 0%{?build_gui}
%files gui -f %{name}.lang
%doc gui/{AUTHORS,README*,TODO}
%license gui/COPYING*
%{_bindir}/gpsbabelfe-bin
%{_datadir}/gpsbabel
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/256x256/apps/*
%endif

%changelog
* Mon Apr 01 2019 Justin Bronn <justin.bronn@radiantsolutions.com> - 1.5.4-1
- Initial Release
