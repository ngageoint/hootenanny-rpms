Name:           armadillo
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Fast C++ matrix library with syntax similar to MATLAB and Octave

License:        ASL 2.0
URL:            https://arma.sourceforge.net/
Source:         https://sourceforge.net/projects/arma/files/%{name}-%{version}.tar.xz

BuildRequires:  arpack-devel
BuildRequires:  atlas-devel
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  hdf5-devel
BuildRequires:  lapack-devel
BuildRequires:  openblas-devel
BuildRequires:  SuperLU-devel


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
%setup -q

# convert DOS end-of-line to UNIX end-of-line

for file in README.md; do
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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%{_libdir}/libarmadillo.so.9*
%license LICENSE.txt NOTICE.txt


%files devel
%{_libdir}/libarmadillo.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/armadillo
%{_includedir}/armadillo_bits/
%{_datadir}/Armadillo/
%doc README.md index.html docs.html
%doc examples armadillo_icon.png
%doc armadillo_nicta_2010.pdf rcpp_armadillo_csda_2014.pdf
%doc armadillo_joss_2016.pdf arma_spmat_icms_2018.pdf
%doc mex_interface


%changelog
* Fri May 24 2019 Justin Bronn <justin.bronn@radiantsolutions.com> - 9.400.3-1
- Initial release: 9.400.3.
