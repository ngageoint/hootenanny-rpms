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
Name:           libpostal
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Group:          Applications/Engineering
Summary:        C library for parsing/normalizing street addresses around the world
License:        MIT
URL:            https://github.com/openvenues/libpostal/
Source0:        https://github.com/openvenues/libpostal/archive/v%{version}/libpostal-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig

%description
A C library for parsing/normalizing street addresses around the world using
statistical NLP and open data. The goal of this project is to understand
location-based strings in every language, everywhere. 


%package devel
Summary:        Development headers and files for libpostal
Requires:       %{name}%{_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and headers for developing
applications which use the libphonenumber C library.


%prep
%setup -q


%build
./bootstrap.sh
%{configure} --disable-data-download
%{make_build}


%install
%{makeinstall}


%check


%files


%files devel



%changelog
* Thu Nov 08 2018 Justin Bronn <justin.bronn@radiantsolutions.com> - 1.0.0-1
- Initial release, 1.0.0.
