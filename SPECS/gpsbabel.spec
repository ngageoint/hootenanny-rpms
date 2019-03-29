Name:          gpsbabel
Version:       1.5.4
Release:       13%{?dist}
Summary:       A tool to convert between various formats used by GPS devices

License:       GPLv2+
URL:           http://www.gpsbabel.org
# Upstream's website hides tarball behind some ugly php script
# Original repo is at https://github.com/gpsbabel/gpsbabel
Source0:       %{name}-%{version}.tar.gz
Source2:       %{name}.png
Source21:      http://www.gpsbabel.org/style3.css
# Remove network access requirement for XML doc builds and HTML doc reading
Patch1:        0001-gpsbabel-1.4.2-xmldoc.patch
# Use system shapelib - not suitable for upstream in this form.
Patch2:        0002-gpsbabel-1.4.3-use-system-shapelib.patch
# Pickup gmapbase.html from /usr/share/gpsbabel
Patch3:        0003-gpsbabel-1.4.3-gmapbase.patch
# No automatic phone home by default (RHBZ 668865)
Patch4:        0004-gpsbabel-1.4.3-nosolicitation.patch
# Use system zlib
Patch5:        0005-Use-system-zlib.patch
# Use system minizip
Patch6:        0006-Use-system-minizip.patch
# Upstream patch
Patch7:        0007-Added-geojson-read-capablity-moved-magic-strings-to-.patch
# RHBZ#1561337
Patch8:        0008-Correctly-read-diff-and-terr-from-geo-format.patch
# RHBZ#1625204
Patch9:        0009-Remove-SHAPE-ZLIB-MINIZIP-from-LIBOBJS.patch

BuildRequires: %{__make}
BuildRequires: %{__perl}

BuildRequires: expat-devel
BuildRequires: libusb-devel
BuildRequires: zlib-devel
BuildRequires: minizip-compat-devel
BuildRequires: qt5-qtbase-devel

# https://fedoraproject.org/wiki/Changes/RemoveObsoleteScriptlets
%if !((0%{?fedora} >= 28) || (0%{?rhel} >= 8))
%{error:No gtk-update-icon-cache scriptlets for Fedora prior to F28 or EL prior to EL8.}
%endif

%if 0%{?fedora}
%if 0%{?fedora} >= 27
%ifarch %{qt5_qtwebengine_arches}
# HACK: Don't build GUI on archs not supported by qtwebengine
%global QT_GUI  qtwebengine
%endif
%else
# Fedora <= 26 used qtwebkit; Try to stay backward compatible
%global QT_GUI  qtwebkit
%endif
%endif

%if 0%{?el7}
# FIXME: epel7 doesn't have qtwebengine
# Fall back to qtwebkit
%global QT_GUI  qtwebkit
%endif

%if "%{?QT_GUI}"
%global build_gui 1
BuildRequires: qt5-%{QT_GUI}-devel
BuildRequires: /usr/bin/lrelease-qt5
%endif

BuildRequires: desktop-file-utils
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
BuildRequires: shapelib-devel

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
%{qmake_qt5} USE_GUI=%{?QT_GUI}
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
* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 05 2018 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.4-12
- Add 0009-Remove-SHAPE-ZLIB-MINIZIP-from-LIBOBJS.patch (RHBZ#1625204).

* Tue Aug 28 2018 Patrik Novotný <panovotn@redhat.com> - 1.5.4-11
- change requires to minizip-compat(-devel) rhbz#1609830, rhbz#1615381

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 03 2018 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.4-9
- Add 0008-Correctly-read-diff-and-terr-from-geo-format.patch (RHBZ#1561337)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 14 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.4-7
- Re-add non-gui-packages on Archs not supported by qtwebengine (RHBZ#1481163).

* Mon Aug 07 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.4-6
- Add 0007-Added-geojson-read-capablity-moved-magic-strings-to-.patch (F27FTBFS).
- Switch to using qtwebengine on Fedora >= 27.
  Drop archs not supporting qtwebengine.

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.4-2
- Switch back to qtwebkit on Fedora <= 26.

* Sun Jan 15 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.4-1
- Update to gpsbabel-1.5.4.
- Rebase patches.
- Build against qt5/qt5-qtwebengine.
- Use %%qt5_translationdir.
- Misc. *spec cleanup.

* Sun Dec 11 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.3-6
- Add %%{__make}, %%{__perl}.

* Sun Dec 11 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.5.3-5
- Rebuild for shapelib SONAME bump

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Feb 02 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.5.3-3
- use %%qmake_qt4 macro to ensure proper build flags

* Wed Jan 27 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.3-2
- Add %%license to *-gui.

* Thu Jan 07 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.3-1
- Upstream update.
- Rebase patches.
- Reflect upstream shipping malpackaged tarballs.
- Unbundle minizip.
- Remove gpsbabel-tarball.
- Introduce %%license.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.5.2-2
- Rebuilt for GCC 5 C++11 ABI change

* Fri Jan 09 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.2-1
- Upstream update.
- Rebase patches.
- Reflect upstream having stopped providing tarballs:
  - Add gpsbabel-tarball.
  - Remove gpsbabel-download-latest.py.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 16 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.5.0-1
- Update to 1.5.0.
- Rebase/rework patches.
- Rework spec.

* Tue Apr 15 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.4.4-6
- Update gpsbabel-1.4.3-use-system-shapelib.patch to fix FTBFS.
- More spec modernization.

* Wed Jul 31 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.4.4-5
- Modernize spec.
- Drop Fedora < 14.
- Really apply patch25 (missed in *-3).
- Fix broken %%changelog date.

* Tue Jul 30 2013 Conrad Meyer <cemeyer@uw.edu> - 1.4.4-4
- Fix Garmin .fit file handling (RHBZ 989851).

* Sun Mar 24 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.4.4-3
- Add aarch64 (RHBZ 925480).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 17 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.4.4-1
- Upstream update.
- Rebase patches.
- Use upstream gpsbabel.desktop.
- Address RHBZ 668865.
- Fix gzFile pointer abuse.
- Install gmapbase.html to /usr/share/gpsbabel.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.4.2-6
- Rebuild for libusb-config (#715220)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Hans Ulrich Niedermann <hun@n-dimensional.de> - 1.4.2-4
- Have this spec file build on f12,f13,f14,f15,el6. (el6 without GUI).
- Rename local copy of style3.css
- Ship translations for the GUI
- Enforce network less doc build with xsltproc --nonet

* Tue Jan 11 2011 Hans Ulrich Niedermann <hun@n-dimensional.de> - 1.4.2-2
- Shut up desktop-file-install warnings
- Comment the patches in the spec file

* Tue Jan 11 2011 Hans Ulrich Niedermann <hun@n-dimensional.de> - 1.4.2-1
- Update to 1.4.2
- Document how to get source tarball via HTTP POST
- Use Fedora's system shapelib instead of gpsbabel's bundled shapelib parts
- Use new mktemp based BuildRoot
- Build and view gpsbabel.html without network access
- Avoid rpm macros for scriptlet commands
- Remove x bit also from src files in subdirectories
- Add Additional Category to .desktop file: Geography

* Fri Sep 17 2010 Mikhail Kalenkov <mikhail.kalenkov@gmail.com> - 1.4.1-2
- build documentation (gpsbabel.html)

* Thu Sep 16 2010 Mikhail Kalenkov <mikhail.kalenkov@gmail.com> - 1.4.1-1
- update to 1.4.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 05 2008 Douglas E. Warner <silfreed@silfreed.net> - 1.3.6-1
- update to 1.3.6

* Fri May 09 2008 Douglas E. Warner <silfreed@silfreed.net> - 1.3.5-1
- update to 1.3.5
- switching out variables for macros; adding macros for commands
- fixing license to be GPLv2+
- adding patch to fix re-running autoconf
- perserving times when installing gpsbabel

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.4-2
- Autorebuild for GCC 4.3

* Tue Dec 18 2007 Douglas E. Warner <silfreed@silfreed.net> - 1.3.4-1
- Update to 1.3.4

* Thu Apr 19 2007 Roozbeh Pournader <roozbeh@farsiweb.info> - 1.3.3-1
- Make first Fedora spec based on the one provided upstream
