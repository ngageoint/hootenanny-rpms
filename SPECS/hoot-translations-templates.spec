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

%global hoot_home %{_sharedstatedir}/hootenanny

Name:        hoot-translations-templates
Version:     %{rpmbuild_version}
Release:     %{rpmbuild_release}%{?dist}
Summary:     Hootenanny Translations Templates

Group:       Applications/Engineering
License:     Proprietary
URL:         https://github.com/ngageoint/hootenanny

Source0:     tds40.tgz
Source1:     tds61.tgz

BuildArch:   noarch
AutoReqProv: no


%description
Supplementary translations template files for use with Hootenanny.


%prep


%build


%install
%{__install} -d -m 0755 %{buildroot}%{hoot_home}/translations/templates
%{__install} -m 0644 %{SOURCE0} %{buildroot}%{hoot_home}/translations/templates
%{__install} -m 0644 %{SOURCE1} %{buildroot}%{hoot_home}/translations/templates


%files
%{hoot_home}/translations/templates


%changelog
* Fri Nov 09 2018 Justin Bronn <justin.bronn@radiantsolutions.com> - 1.0.0-1
- Initial release, 1.0.0.
