Name: log4cxx
Version: 0.10.0
Release: 14%{?dist}
Summary: A port to C++ of the Log4j project

Group: System Environment/Libraries
License: ASL 2.0
URL: http://logging.apache.org/log4cxx/index.html
Source0: http://www.apache.org/dist/logging/log4cxx/%{version}/apache-%{name}-%{version}.tar.gz
# Filed into upstream bugtracker at:
# https://issues.apache.org/jira/browse/LOGCXX-332
Patch0: log4cxx-cstring.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: apr-devel,apr-util-devel,doxygen

%description
Log4cxx is a popular logging package written in C++. One of its distinctive
features is the notion of inheritance in loggers. Using a logger hierarchy it
is possible to control which log statements are output at arbitrary
granularity. This helps reduce the volume of logged output and minimize the
cost of logging.

%prep
%setup -q -n apache-%{name}-%{version}
%patch0 -p1

%build
sed -i.libdir_syssearch -e \
 '/sys_lib_dlsearch_path_spec/s|/usr/lib |/usr/lib /usr/lib64 /lib /lib64 |' \
 configure
%configure
make -k %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/html .

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/liblog4cxx.so.10.0.0
%{_libdir}/liblog4cxx.so.10

%doc NOTICE LICENSE KEYS

%package devel
Requires: %{name} = %{version}-%{release},pkgconfig,apr-devel
Group: Development/Libraries
Summary: Header files for Log4xcc - a port to C++ of the Log4j project

%description devel
Header files and documentation you can use to develop with log4cxx

%files devel
%defattr(-,root,root,-)
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.a
%{_includedir}/log4cxx
%{_libdir}/liblog4cxx.so
%{_libdir}/pkgconfig/liblog4cxx.pc

%doc html/

%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-12
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 01 2009 Caolán McNamara <caolanm@redhat.com> - 0.10.0-9
- Rebuild for new db4

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 25 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 0.10.0-7
- Fix FTBFS: updated log4cxx-cstring.patch for gcc 4.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 1 2008 Hayden James - 0.10.0-5
- Simplifed doc files in package

* Sat Nov 29 2008 Hayden James - 0.10.0-4
- Moved doxygen docs into doc folder 
- Removed unnecessary apr-util-devel dependency

* Thu Nov 27 2008 Hayden James - 0.10.0-3
- Remove need for chrpath and other misc changes.

* Thu Nov 27 2008 Hayden James - 0.10.0-2
- Build requires doxygen for documentation

* Sun Nov 16 2008 Hayden James - 0.10.0-1
- Initial package.

