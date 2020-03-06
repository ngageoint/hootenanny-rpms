# Copyright (C) 2018, 2019, 2020 Maxar Technologies (https://www.maxar.com)
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

%global hoot_home %{_sharedstatedir}/hootenanny
%global hoot_translations_local %{hoot_home}/translations-local

# Don't bytecompile Python files.
%global __os_install_post %(echo '%{__os_install_post}' | %{__sed} -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

Name:        hoot-translations
Version:     %{rpmbuild_version}
Release:     %{rpmbuild_release}%{?dist}
Summary:     Hootenanny Translations Templates

License:     Proprietary
URL:         https://github.com/ngageoint/hootenanny

Source0:     hootenanny-translations-%{version}.tar.gz

BuildArch:   noarch
AutoReqProv: no


%description
Supplementary translations template files for use with Hootenanny.


%prep
%autosetup -n translations-local


%build


%install
%{__install} -d -m 0755 %{buildroot}%{hoot_translations_local}
%{__cp} -rp * %{buildroot}%{hoot_translations_local}


%files
%{hoot_translations_local}


%changelog
* Fri Mar 06 2020 Justin Bronn <justin.bronn@maxar.com> - 1.0.0-1
- Initial release, 1.0.0.
