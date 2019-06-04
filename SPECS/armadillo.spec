Name:           armadillo
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Fast C++ matrix library with syntax similar to MATLAB and Octave

License:        ASL 2.0
URL:            https://arma.sourceforge.net/
Source:         https://sourceforge.net/projects/arma/files/%{name}-%{version}.tar.xz
Patch1:         armadillo-tests-makefile.patch

BuildRequires:  arpack-devel
BuildRequires:  atlas-devel
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  hdf5-devel
BuildRequires:  lapack-devel
BuildRequires:  openblas-devel
BuildRequires:  SuperLU-devel

%global major_version %(echo %{version} | %{__awk} -F. '{ print $1 }')
%if 0%{major_version} >= 9
%global readme_type md
%else
%global readme_type txt
%endif

%description
Armadillo is a C++ linear algebra library (matrix maths)
aiming towards a good balance between speed and ease of use.
Integer, floating point and complex numbers are supported,
as well as a subset of trigonometric and statistics functions.
Various matrix decompositions are provided through optional
integration with LAPACK and ATLAS libraries.
A delayed evaluation approach is employed (during compile time)
to combine several operations into one and reduce (or eliminate)
the need for temporaries. This is accomplished through recursive
templates and template meta-programming.
This library is useful if C++ has been decided as the language
of choice (due to speed and/or integration capabilities), rather
than another language like Matlab or Octave.


%package devel
Summary:        Development headers and documentation for the Armadillo C++ library
Requires:       %{name} = %{version}-%{release}
Requires:       arpack-devel
Requires:       atlas-devel
Requires:       hdf5-devel
Requires:       lapack-devel
Requires:       libstdc++-devel
Requires:       openblas-devel
Requires:       SuperLU-devel


%description devel
This package contains files necessary for development using the
Armadillo C++ library. It contains header files, example programs,
and user documentation (API reference guide).


%prep
%autosetup -p1

# convert DOS end-of-line to UNIX end-of-line

for file in README.%{readme_type}; do
  sed 's/\r//' $file >$file.new && \
  touch -r $file $file.new && \
  mv $file.new $file
done


%build
%{cmake}
%{__make} VERBOSE=1 %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
rm -f examples/Makefile.cmake
rm -f examples/example1_win64.sln
rm -f examples/example1_win64.vcxproj
rm -f examples/example1_win64.README.txt
rm -rf examples/lib_win64


%check
# The armadillo-tests-makefile.patch allows extension of CXX_FLAGS/LIB_FLAGS.
CXX_FLAGS=-I%{buildroot}%{_includedir} LIB_FLAGS=-L%{buildroot}%{_libdir} make -C tests

# Exclude spsolve tests that also fail on 8.300.0 package from EPEL.
LD_LIBRARY_PATH=%{buildroot}%{_libdir} ./tests/main \
  exclude:fn_spsolve_float_function_test \
  exclude:fn_spsolve_sparse_complex_float_test \
  exclude:fn_spsolve_sparse_nonsymmetric_complex_float_test


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%{_libdir}/libarmadillo.so.%{major_version}*
%license LICENSE.txt NOTICE.txt


%files devel
%{_libdir}/libarmadillo.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/armadillo
%{_includedir}/armadillo_bits/
%{_datadir}/Armadillo/
%doc README.%{readme_type} index.html docs.html
%doc examples armadillo_icon.png
%doc *.pdf
%doc mex_interface


%changelog
* Tue Jun 04 2019 Justin Bronn <justin.bronn@radiantsolutions.com> - 8.300.4-1
- Initial release: 8.300.4.
