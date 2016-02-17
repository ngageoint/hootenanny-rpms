Name:		stxxl
Version:	1.3.1
Release:	1%{?dist}
Summary:	C++ STL drop-in replacement for extremely large datasets 

Group:		Development/Libraries	
License:	Boost	
URL:		http://%{name}.sourceforge.net	
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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
make config_gnu

echo STXXL_ROOT	=`pwd` > make.settings.local
echo "ENABLE_SHARED	= yes" >> make.settings.local
echo "COMPILER_GCC	= g++ -std=c++0x" >> make.settings.local
make library_g++

%install
rm -rf %{buildroot} 
# There is no install target provided. However the library consists of a .so and a set of headers. 
# Let us install them, as required

# Install the library
install -p -D -m 0755 lib/libstxxl.so %{buildroot}%{_libdir}/libstxxl.so.%{version}

# Install the header files
mkdir -p %{buildroot}%{_includedir}
cp -pr include/* %{buildroot}%{_includedir}

pushd .
cd %{buildroot}%{_libdir}
#link libSONAME.so.MAJOR to libSONAME.so.MAJOR.MINOR.MICRO
ln -s libstxxl.so.%{version} libstxxl.so.1
#link libSONAME.so to libSONAME.so.MAJOR
ln -s libstxxl.so.1 libstxxl.so
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%doc LICENSE_1_0.txt CHANGELOG TODO README TROUBLESHOOTING 
%{_libdir}/libstxxl.so.*

%files devel
%defattr(-,root,root,-)
%doc config_example
%dir %{_includedir}/bits/
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_includedir}/bits/intel_compatibility.h
%{_libdir}/libstxxl.so

%changelog
* Fri Jan 30 2016 Benjamin Marchant <benjamin.marchant(a!t)digitalglobe.com> 1.3.1-1
- Create spec file

