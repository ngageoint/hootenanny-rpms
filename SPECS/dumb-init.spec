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
Name:		dumb-init
Version:	%{rpmbuild_version}
Release:	%{rpmbuild_release}%{?dist}
Summary:	Simple process supervisor and init system for containers
Group:		Applications/System
License:	MIT
URL:		https://github.com/Yelp/dumb-init
Source0:	https://github.com/Yelp/dumb-init/archive/v%{version}/dumb-init-%{version}.tar.gz

%description
dumb-init is a simple process supervisor that forwards signals to children.
It is designed to run as PID1 in minimal container environments.

%prep
%setup -q

%build
# Remove static compilation flag, as we're only targeting Enterprise Linux
# containers (like the rest of our dependencies).
%{__sed} -i -e 's/ -static//' Makefile
%{__make}

# TODO: Consider substituting hard-coded CFLAGS with `%{optflags}` in Makefile.

%install
# Placing in binary directory as it may be invoked by non-root users.
%{__install} -p -D -m 0755 dumb-init %{buildroot}%{_bindir}/dumb-init

%files
%{_bindir}/dumb-init

%changelog
* Tue Jan 16 2018 Justin Bronn <justin.bronn@digitalglobe.com> 1.2.1-1
- Initial revision.
