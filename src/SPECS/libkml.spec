Name:           libkml
Version:        1.3.0
Release:        1%{?dist}
Summary:        Reference implementation of OGC KML 2.2

License:        BSD
URL:            https://github.com/libkml/libkml
Source0:        https://github.com/libkml/libkml/archive/%{version}/libkml-%{version}.tar.gz

## See https://github.com/libkml/libkml/pull/239
Patch0:         libkml-0001-Fix-build-failure-due-to-failure-to-convert-pointer-.patch
Patch1:         libkml-0002-Fix-mistaken-use-of-std-cerr-instead-of-std-endl.patch
Patch2:         libkml-0003-Fix-python-tests.patch
Patch3:         libkml-0004-Correctly-build-and-run-java-test.patch
# Fix a fragile test failing on i686
Patch4:         libkml-fragile_test.patch
# Don't bytecompile python sources as part of build process, leave it to rpmbuild
Patch5:         libkml-dont-bytecompile.patch

BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  boost-devel
BuildRequires:  expat-devel
BuildRequires:  gtest-devel
BuildRequires:  java-devel
BuildRequires:  junit
BuildRequires:  minizip-devel
%if 0%{?fedora}
BuildRequires:  python2-devel
BuildRequires:  python3-devel
%else
BuildRequires:  python-devel
%endif
BuildRequires:  swig
BuildRequires:  uriparser-devel
BuildRequires:  zlib-devel

%global __requires_exclude_from ^%{_docdir}/.*$
%global __provides_exclude_from ^%{python2_sitearch}/.*\\.so$


%description
Reference implementation of OGC KML 2.2.
#It also includes implementations of Google's gx: extensions used by Google
Earth, as well as several utility libraries for working with other formats.


%package -n python2-%{name}
Summary:        Python 2 bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}}

%description -n python2-%{name}
The python2-%{name} package contains Python 2 bindings for %{name}.


%package -n python3-%{name}
Summary:        Python 3 bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}


%description -n python3-%{name}
The python3-%{name} package contains Python 3 bindings for %{name}.


%package java
Summary:        Java bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description java
The %{name}-java package contains Java bindings for %{name}.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       boost-devel
Requires:       expat-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1


%build

# Allow CMake to proceed with zlib 1.2.7.
sed -i -e 's/ZLIB 1\.2\.8/ZLIB 1\.2\.7/' CMakeLists.txt

mkdir build_py2
pushd build_py2
%ifarch armv7hl
%define awtlib -DJAVA_AWT_LIBRARY=`find /usr/lib/jvm/ -name libjawt.so | grep jre/lib/arm \`
%endif
%cmake -DWITH_SWIG=ON -DWITH_PYTHON=ON -DWITH_JAVA=ON \
  -DJNI_INSTALL_DIR=%{_libdir}/%{name} \
  -DCMAKE_INSTALL_DIR=%{_libdir}/cmake/%{name} \
  -DINCLUDE_INSTALL_DIR=%{_includedir}/kml \
  -DPYTHON_LIBRARY=%{_libdir}/libpython%{python2_version}.so \
  -DPYTHON_INCLUDE_DIR=%{_includedir}/python%{python2_version}/ \
  -DPYTHON_INSTALL_DIR=%{python2_sitearch} \
  %{?awtlib} \
  -DBUILD_TESTING=ON \
  -DBUILD_EXAMPLES=ON \
  ..
%make_build
popd

mkdir build_py3
pushd build_py3
%cmake -DWITH_SWIG=ON -DWITH_PYTHON=ON -DWITH_JAVA=OFF \
  -DJNI_INSTALL_DIR=%{_libdir}/%{name} \
  -DCMAKE_INSTALL_DIR=%{_libdir}/cmake/%{name} \
  -DINCLUDE_INSTALL_DIR=%{_includedir}/kml \
  -DPYTHON_LIBRARY=%{_libdir}/libpython%{python3_version}m.so \
  -DPYTHON_INCLUDE_DIR=%{_includedir}/python%{python3_version}m/ \
  -DPYTHON_INSTALL_DIR=%{python3_sitearch} \
  -DBUILD_TESTING=ON \
  -DBUILD_EXAMPLES=OFF \
  ..
%make_build
popd


%install
%make_install -C build_py2
%make_install -C build_py3


%check
pushd build_py2
ctest -V
popd
pushd build_py3
ctest -V -E test_python_kml
popd


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license LICENSE
%doc AUTHORS README.md
%{_libdir}/libkml*.so.*

%files -n python2-%{name}
%{python2_sitearch}/*.so
%{python2_sitearch}/*.py*

%files -n python3-%{name}
%{python3_sitearch}/*.so
%{python3_sitearch}/*.py
%{python3_sitearch}/__pycache__/*.py*

%files java
%{_javadir}/LibKML.jar
%{_libdir}/%{name}/

%files devel
%doc examples
%{_includedir}/kml/
%{_libdir}/libkml*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/

%changelog
* Mon Aug 07 2017 Sandro Mani <manisandro@gmail.com> - 1.3.0-8
- Workaround armv7hl FTBFS
- Add python3 bindings

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 18 2017 Jonathan Wakely <jwakely@redhat.com> - 1.3.0-5
- Rebuilt for Boost 1.64

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Apr 08 2016 Sandro Mani <manisandro@gmail.com> - 1.3.0-2
- Don't call it Google's reference implementation in Summary/Description
- Update Source URL
- Add python_provide macro
- Enable tests

* Thu Mar 31 2016 Sandro Mani <manisandro@gmail.com> - 1.3.0-1
- Update to 1.3.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 02 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.6.1-7
- Fix gcc warning that lead to failure due to -Werror flag

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 12 2009 Rakesh Pandit <rakesh@fedoraproject.org> 0.6.1-4
- Included *pyc and pyo files in %%files and added BuildRequires libgcj-devel.

* Sun Apr 12 2009 Rakesh Pandit <rakesh@fedoraproject.org> 0.6.1-3
- libkml-0.6.1.configure_ac.patch patch for swig > 1.3.35

* Sat Mar 07 2009 Rakesh Pandit <rakesh@fedoraproject.org> 0.6.1-2
- updated to 0.6.1
- libkml-third_party_removal.diff Removes third part dependency
- (provided by Peter Lemenkov)

* Fri Jan 16 2009 Rakesh Pandit <rakesh@fedoraproject.org> 0.6.1-1
- Updated to 0.6.1

* Mon Oct 06 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.4.0-2
- Added >= 1.3.35 for swing

* Sat Aug 09 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.4.0-1
- Initial package
