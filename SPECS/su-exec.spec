Name:		su-exec
Version:	%{rpmbuild_version}
Release:	%{rpmbuild_release}%{?dist}
Summary:	Simple tool to execute as another user and group
Group:		Applications/System
License:	MIT
URL:		https://github.com/ncopa/su-exec
Source0:	https://github.com/ncopa/su-exec/archive/v%{version}/su-exec-%{version}.tar.gz

%description
This is a simple tool that will simply execute a program with different
privileges. The program will not run as a child, like su and sudo, so
we work around TTY and signal issues.  C implementation of tianon/gosu.

%prep
%setup -q

%build
%{__make}

%install
%{__install} -p -D -m 0755 su-exec %{buildroot}%{_sbindir}/su-exec

%files
%{_sbindir}/su-exec

%changelog
* Tue Jan 2 2018 Justin Bronn <justin.bronn@digitalglobe.com> 0.2-1
- Initial revision.
