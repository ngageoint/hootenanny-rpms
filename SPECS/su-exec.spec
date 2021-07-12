# Copyright (C) 2018 Radiant Solutions (http://www.radiantsolutions.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
