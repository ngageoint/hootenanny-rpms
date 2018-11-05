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
