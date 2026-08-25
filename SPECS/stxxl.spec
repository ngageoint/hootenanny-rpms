Name:		stxxl
Version:	%{rpmbuild_version}
Release:	%{rpmbuild_release}%{?dist}
Summary:	C++ STL drop-in replacement for extremely large datasets

Group:		Development/Libraries
License:	Boost
URL:		http://%{name}.sourceforge.net
Source0:	https://github.com/stxxl/stxxl/archive/refs/tags/%{version}.tar.gz
%global __cmake_builddir build

%global _smp_mflags -j%(nproc)

%description
%{name} provides an STL replacement using an abstraction layer to
storage devices to allow for the optimal layout of data structures. This
allows for multi-terabyte datasets to be held and manipulated in standard
C++ data structures, whilst abstracting the complexity of managing this
behaviour efficiently. %{name} utilises multi-disk I/O to speed up
I/O bound calculations. STXXL has been developed at the University
of Karlsruhe.

%package devel
Group:		Development/Libraries
Summary:	Provides development files for %{name} applications
Requires:	%{name} = %{version}-%{release}

%description devel
Development libraries for the %{name} library.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DINSTALL_LIB_DIR=/usr/lib64 -DINSTALL_PKGCONFIG_DIR=/usr/lib64/pkgconfig -DINSTALL_CMAKE_DIR=/usr/lib64/cmake/stxxl
%cmake_build

%install
%cmake_install

%files
%license LICENSE_1_0.txt
%doc CHANGELOG TODO README
%{_libdir}/libstxxl.so.1.4.1
%{_bindir}/stxxl_tool

%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}
%{_libdir}/libstxxl.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libstxxl.a
%{_libdir}/cmake/stxxl

%changelog
* Wed Aug 12 2026 Leia <leia@vantor.com> - 1.4.1-1
- Rebase to CMake build system for RHEL 9 / Rocky 9. Drop CentOS7-only
  mlock.cpp sed patch (not applicable to CMake build). Version bump
  from 1.3.1.
* Sat Jan 30 2016 Benjamin Marchant <benjamin.marchant(a!t)digitalglobe.com> 1.3.1-1
- Create spec file
