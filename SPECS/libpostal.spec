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

# Enable fetch of the source by rpmbuild (libpostal data files are
# too large to host in the repository).
%undefine _disable_source_fetch

# The libpostal data directory, this global path *must* be writable by
# the user invoking `rpmbuild` in order to run the tests.
%global libpostal_data %{_datadir}/libpostal

# By default, run the test suite.
%bcond_without tests

# When enabled, don't force use of -O0 optimization on the scanner file.
# This will make compilation take a *long* time (~1 hour).
%bcond_with optimize_scanner

# The latest version of libpostal doesn't provide a new version of parser,
# language_classifier, or libpostal_data, grab them from a previous version
%global parser_version 1.0.0


Name:           libpostal
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Group:          Applications/Engineering
Summary:        C library for parsing/normalizing street addresses around the world
License:        MIT
URL:            https://github.com/openvenues/libpostal/
Source0:        https://github.com/openvenues/libpostal/archive/refs/tags/v%{version}.tar.gz
Source1:        https://github.com/openvenues/libpostal/releases/download/v%{parser_version}/parser.tar.gz
Source2:        https://github.com/openvenues/libpostal/releases/download/v%{parser_version}/language_classifier.tar.gz
Source3:        https://github.com/openvenues/libpostal/releases/download/v%{parser_version}/libpostal_data.tar.gz

# Modify build system to accomodate RPM build flags.
Patch0:         libpostal-configure.patch
# Calling `crf_context_destroy` at end of tests will cause a segfault,
# must patch in order to run the test suite.
Patch1:         libpostal-tests-fix.patch
# Don't use -O0 when compiling the scanner.
Patch2:         libpostal-optimize-scanner.patch

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
BuildArch:      noarch

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
%if %{with tests}
%patch1 -p1
%endif
%if %{with optimize_scanner}
%patch2 -p1
%endif


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


%if %{with tests}
%check
# Link in datafiles from the buildroot to the global data directory.
%{__mkdir_p} %{libpostal_data}
%{__rm} -f %{libpostal_data}/*
find %{buildroot}%{libpostal_data} -maxdepth 1 -type d -exec ln -s {} %{libpostal_data} \;
%{__make} check
%endif


%files
%doc README.md
%license LICENSE
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
* Wed Oct 12 2022 Ben Marchant <benjamin.marchant@maxar.com> - 1.1-1
- Updated release, 1.1
* Thu Nov 08 2018 Justin Bronn <justin.bronn@radiantsolutions.com> - 1.0.0-1
- Initial release, 1.0.0.
