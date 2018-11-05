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
Name:           libphonenumber
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Group:          Applications/Engineering
Summary:        C++ library for parsing, formatting, and validating phone numbers.
License:        ASL 2.0 and BSD and MIT
URL:            https://github.com/googlei18n/libphonenumber/
Source0:        https://github.com/googlei18n/libphonenumber/archive/v%{version}/libphonenumber-%{version}.tar.gz

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gtest-devel
BuildRequires:  libicu-devel
BuildRequires:  protobuf
BuildRequires:  protobuf-compiler
BuildRequires:  protobuf-devel
BuildRequires:  re2-devel

%description
The Google common Java, C++ and JavaScript library for parsing, formatting, and
validating international phone numbers.


%package devel
Summary:        Development headers and files for libphonenumber
Requires:       %{name}%{_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and headers for developing
applications which use the Google libphonenumber C++ library.


%prep
%setup -q


%build
%{__mkdir_p} cpp/build
pushd cpp/build
%{cmake} ..
%{make_build}


%check
# Run the compiled tests.
./cpp/build/geocoding_test_program
./cpp/build/libphonenumber_test


%install
%{__make} -C cpp/build install DESTDIR=%{buildroot}


%files
%doc FAQ.md README.md
%license LICENSE LICENSE.Chromium
%{_libdir}/*.so.*
%exclude %{_libdir}/*.a


%files devel
%doc AUTHORS CONTRIBUTORS CONTRIBUTING.md
%{_includedir}/phonenumbers
%{_libdir}/*.so


%changelog
* Tue Nov 06 2018 Justin Bronn <justin.bronn@radiantsolutions.com> - 8.9.16-1
- Initial release, 8.9.16.
