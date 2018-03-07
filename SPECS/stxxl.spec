Name:		stxxl
Version:	%{rpmbuild_version}
Release:	%{rpmbuild_release}%{?dist}
Summary:	C++ STL drop-in replacement for extremely large datasets

Group:		Development/Libraries
License:	Boost
URL:		http://%{name}.sourceforge.net
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

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
%setup -q

%build
# Configure
%{__make} config_gnu

%{__cat} > make.settings.local <<EOF
STXXL_ROOT	= $(pwd)
ENABLE_SHARED	= yes
COMPILER_GCC	= g++ -std=c++0x
EOF

# Total hack because 1.3.1 doesn't compile right on CentOS7
%{__sed} -i 's/#include <sys\/mman.h>/#include <sys\/mman.h>\n#include <unistd.h>/g' ./utils/mlock.cpp

%{__make} library_g++

%install
# There is no install target provided. However the library consists of a .so
# and a set of headers.  Let us install them, as required

# Install the library
%{__install} -p -D -m 0755 lib/libstxxl.so %{buildroot}%{_libdir}/libstxxl.so.%{version}

# Install the header files
%{__mkdir} -p %{buildroot}%{_includedir}
%{__cp} -pr include/* %{buildroot}%{_includedir}

pushd %{buildroot}%{_libdir}
#link libSONAME.so.MAJOR to libSONAME.so.MAJOR.MINOR.MICRO
%{__ln_s} libstxxl.so.%{version} libstxxl.so.1
#link libSONAME.so to libSONAME.so.MAJOR
%{__ln_s} libstxxl.so.1 libstxxl.so
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE_1_0.txt CHANGELOG TODO README TROUBLESHOOTING
%{_libdir}/libstxxl.so.1
%{_libdir}/libstxxl.so.%{version}

%files devel
%defattr(-,root,root,-)
%doc config_example
%dir %{_includedir}/bits
%{_includedir}/%{name}.h
%{_includedir}/%{name}
%{_includedir}/bits/intel_compatibility.h
%{_libdir}/libstxxl.so

%changelog
* Sat Jan 30 2016 Benjamin Marchant <benjamin.marchant(a!t)digitalglobe.com> 1.3.1-1
- Create spec file
