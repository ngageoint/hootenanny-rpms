# Copyright (C) 2018-2021 Maxar Technologies, Inc. (https://www.maxar.com)
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

%global __cmake_builddir build
%global _smp_mflags -j%(nproc)

Name:           protobuf
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Group:          Development/Libraries
Summary:        Protocol Buffers - Google's data interchange format
License:        BSD
URL:            https://github.com/protocolbuffers/protobuf
Source0:        https://github.com/protocolbuffers/protobuf/releases/download/v%{version}/protobuf-cpp-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  zlib-devel

%description
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

%package compiler
Summary:        Protocol Buffers compiler (protoc)
Requires:       %{name}%{_isa} = %{version}-%{release}

%description compiler
The %{name}-compiler package contains the protoc compiler used to
generate source code from .proto files.

%package devel
Summary:        Development headers and files for protobuf
Requires:       %{name}%{_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and headers for developing
applications which use the Google Protocol Buffers C++ library.

%prep
%autosetup -n protobuf-%{version} -p1

%build
%cmake -S cmake -B %{__cmake_builddir} \
    -Dprotobuf_BUILD_TESTS=OFF \
    -Dprotobuf_BUILD_SHARED_LIBS=ON \
    -DCMAKE_INSTALL_LIBDIR=%{_lib}
%cmake_build

%install
%cmake_install

# CMake install doesn't ship headers - copy them by hand, public headers only.
mkdir -p %{buildroot}%{_includedir}/google/protobuf
find src/google/protobuf -type f \( -name '*.h' -o -name '*.inc' \) \
    -not -path '*/testing/*' -not -name '*test*' \
    | while read -r f; do
        dest="%{buildroot}%{_includedir}/${f#src/}"
        mkdir -p "$(dirname "$dest")"
        install -p -m 0644 "$f" "$dest"
    done

%files
%license LICENSE
%{_libdir}/*.so.*

%files compiler
%{_bindir}/protoc*

%files devel
%{_includedir}/google
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/protobuf

%changelog
* Wed Aug 12 2026 Leia <leia@vantor.com> - 3.17.3-1
- Initial RHEL 9 / Rocky 9 spec, built via CMake. Headers installed
  manually since upstream's CMake install rules don't ship them.
