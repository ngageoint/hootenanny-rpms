# Copyright (C) 2018 Radiant Solutions (http://www.radiantsolutions.com)
# Copyright (C) 2017 DigitalGlobe (http://www.digitalglobe.com)
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

# Enable fetch of the source by rpmbuild, as it's too big to keep in VCS.
%undefine _disable_source_fetch
%{!?hoot_home: %global hoot_home %{_sharedstatedir}/hootenanny}
%global hoot_dict %{hoot_home}/conf/dictionary
%global words_checksum ac1c4597c7e1efc4c16979d0c92def1d523bbb75f26294026086ee9820a03ee2
%global words_file words1.sqlite

Name:		hoot-words
Version:	%{rpmbuild_version}
Release:	%{rpmbuild_release}%{?dist}
Group:		Applications/Engineering
Summary:	Hootenanny words dictionary
License:	GPLv3
URL:		https://github.com/ngageoint/hootenanny
Source0:	https://s3.amazonaws.com/hoot-rpms/support-files/%{words_file}.bz2
BuildArch:	noarch
BuildRequires:	bzip2
BuildRequires:	coreutils

%description

%prep

%build
# Verify checksum of the downloaded source dictionary file and extract.
%{_bindir}/echo '%{words_checksum}  %{SOURCE0}' | %{_bindir}/sha256sum -c -
%{_bindir}/bzcat %{SOURCE0} > %{words_file}

%install
%{__install} -m 0755 -d %{buildroot}%{hoot_dict}
%{__install} -m 0644 %{words_file} %{buildroot}%{hoot_dict}
pushd %{buildroot}%{hoot_dict}
%{__ln_s} %{words_file} words.sqlite
popd

%clean
%{__rm} -rf %{buildroot}

%files
%{hoot_dict}/%{words_file}
%{hoot_dict}/words.sqlite

%changelog
* Mon Jan 22 2018 Justin Bronn <justin.bronn@digitalglobe.com> - 1.0.1-1
- Fix the directory of the dictionary file.
- Verify dictionary file download with sha256 checksum.
* Wed Nov 15 2017 Justin Bronn <justin.bronn@digitalglobe.com> - 1.0.0-1
- Changed package name to hoot-words.
* Wed Feb 10 2016 Benjamin Marchant <benjamin.marchant@digitalglobe.com> - 1.0.0+
- Initial RPM creation
