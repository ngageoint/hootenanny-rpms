# Copyright (C) 2019 Maxar Technologies (https://www.maxar.com)
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
License:	MIT
URL:		https://github.com/Yelp/dumb-init
Source0:	https://github.com/Yelp/dumb-init/archive/v%{version}/dumb-init-%{version}.tar.gz

%description
dumb-init is a simple process supervisor that forwards signals to children,
and designed to run as PID 1 in minimal container environments.

%prep
%setup -q

%build
# Allow overriding of the CFLAGS environment variable so we can use
# standard compilation options (including hardening).
%{__sed} -i -e 's/^CFLAGS=/CFLAGS\ \?=\ /' Makefile
CFLAGS="%{optflags}" %make_build

%install
# Placing in binary directory as it may be invoked by non-root users.
%{__install} -p -D -m 0755 dumb-init %{buildroot}%{_bindir}/dumb-init

%files
%doc CONTRIBUTING.md README.md
%license LICENSE
%{_bindir}/dumb-init

%changelog
* Thu Mar 11 2021 Justin Bronn <justin.bronn@maxar.com> - 1.2.5-1
- Upgrade to 1.2.5
* Fri Jul 19 2019 Justin Bronn <justin.bronn@maxar.com> 1.2.2-1
- Upgrade to 1.2.2.
* Tue Jan 16 2018 Justin Bronn <justin.bronn@digitalglobe.com> 1.2.1-1
- Initial revision.
