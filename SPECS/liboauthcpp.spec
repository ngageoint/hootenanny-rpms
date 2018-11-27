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
Name:           liboauthcpp
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Group:          Applications/Engineering
Summary:        A pure C++ OAuth library
License:        MIT
URL:            https://github.com/sirikata/liboauthcpp/

# There are no official releases for this library yet.  Create source
# archive from a git checkout of master with the following command
# (set $VERSION to the value you desire):
#
#  git archive \
#    --prefix liboauthcpp-$VERSION/ \
#    --output hootenanny-rpms/SOURCES/liboauthcpp-$VERSION.tar.gz \
#    master
#
Source0:        liboauthcpp-%{version}.tar.gz

# Create a shared library instead of static, and properly set the
# library directory to /usr/lib64.
Patch0:         liboauthcpp-shared-library.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++

%description
liboauthcpp is a pure C++ library for performing OAuth requests. It
does not contain any networking code -- you provide for performing HTTP
requests yourself, however you like -- instead focusing on performing
OAuth-specific functionality and providing a nice interface for it.


%package devel
Summary:        Development headers and files for liboauthcpp
Requires:       %{name}%{_isa} = %{version}-%{release}

%description devel
The liboauthcpp-devel package contains libraries and headers for developing
applications which use the liboauthcpp C++ library.


%prep
%setup -q
%patch0 -p1


%build
pushd build
%{cmake} .
%{make_build}
popd


%check
%{__make} -C build test


%install
%{__make} -C build install DESTDIR=%{buildroot}


%files
%doc README.md
%license LICENSE
%{_libdir}/*.so.*


%files devel
%{_includedir}/liboauthcpp
%{_libdir}/*.so


%changelog
* Thu Nov 15 2018 Justin Bronn <justin.bronn@radiantsolutions.com> - 0.1.0-1
- Initial release, 0.1.0.
