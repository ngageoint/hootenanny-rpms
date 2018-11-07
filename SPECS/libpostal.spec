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

# Enable fetch of the source by rpmbuild.
%undefine _disable_source_fetch

# The libpostal data directory, this global path *must* be writable by
# the user invoking `rpmbuild` in order to run the tests.
%global libpostal_data %{_datadir}/libpostal

Name:           libpostal
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Group:          Applications/Engineering
Summary:        C library for parsing/normalizing street addresses around the world
License:        MIT
URL:            https://github.com/openvenues/libpostal/
Source0:        https://github.com/openvenues/libpostal/archive/v%{version}/libpostal-%{version}.tar.gz
Source1:        https://github.com/openvenues/libpostal/releases/download/v%{version}/parser.tar.gz
Source2:        https://github.com/openvenues/libpostal/releases/download/v%{version}/language_classifier.tar.gz
Source3:        https://github.com/openvenues/libpostal/releases/download/v%{version}/libpostal_data.tar.gz

# Modify build system to accomodate RPM build flags.
Patch0:         libpostal-configure.patch

# Calling `crf_context_destroy` at end of tests will cause a segfault,
# must patch in order to run the test suite.
Patch1:         libpostal-tests-fix.patch

BuildRequires:  atlas-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig

%description
A C library for parsing/normalizing street addresses around the world using
statistical NLP and open data. The goal of this project is to understand
location-based strings in every language, everywhere.


%package data
Summary:        Data files and training models for libpostal
Requires:       %{name}%{_isa} = %{version}-%{release}

%description data
The data files are on-disk representations of the data structures necessary to
perform address expansion as well as model training data.


%package devel
Summary:        Development headers and files for libpostal
Requires:       %{name}%{_isa} = %{version}-%{release}

%description devel
Contains libraries and headers for developing applications which use the
libpostal library.


%prep
%setup -q
%patch0 -p1
%patch1 -p1


%build
./bootstrap.sh
%{configure} --disable-data-download
%{make_build}



%install
%{makeinstall}
# Extract the data files in the buildroot.
%{__install} -d -m 0755 %{buildroot}%{libpostal_data}
%{__tar} -C %{buildroot}%{libpostal_data} -xzf %{SOURCE1}
%{__tar} -C %{buildroot}%{libpostal_data} -xzf %{SOURCE2}
%{__tar} -C %{buildroot}%{libpostal_data} -xzf %{SOURCE3}


%check
# Link in datafiles from the buildroot to the global data directory.
%{__mkdir_p} %{libpostal_data}
%{__rm} -f %{libpostal_data}/*
find %{buildroot}%{libpostal_data} -maxdepth 1 -type d -exec ln -s {} %{libpostal_data} \;
%{__make} check


%files
%{_bindir}/libpostal_data
%{_libdir}/*.so.*
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.a


%files data
%{libpostal_data}


%files devel
%{_includedir}/libpostal
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Thu Nov 08 2018 Justin Bronn <justin.bronn@radiantsolutions.com> - 1.0.0-1
- Initial release, 1.0.0.
