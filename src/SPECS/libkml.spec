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
BuildRequires:  python-devel
BuildRequires:  python34-devel
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
* Wed Nov 15 2017 Justin Bronn <justin.bronn@digitalglobe.com> - 1.3.0-1
- Initial release for use with Hootenanny.
