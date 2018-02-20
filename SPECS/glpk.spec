Name:           glpk
Version:        4.64
Release:        1%{?dist}
Summary:        GNU Linear Programming Kit

License:        GPLv3+
URL:            https://www.gnu.org/software/glpk/glpk.html
Source0:        https://ftp.gnu.org/gnu/glpk/glpk-%{version}.tar.gz
# Un-bundle zlib (#1102855) and suitesparse. Upstream won't accept;
# they want to be ANSI-compatible, and zlib makes POSIX assumptions.
Patch0:         %{name}-unbundle-suitesparse-zlib.patch
# Fix violations of the ANSI C strict aliasing rules
Patch1:         %{name}-alias.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gmp-devel
BuildRequires:  suitesparse-devel
BuildRequires:  zlib-devel

Provides:       bundled(minisat) = 1.14.1

%description
The GLPK (GNU Linear Programming Kit) package is intended for solving
large-scale linear programming (LP), mixed integer programming (MIP),
and other related problems. It is a set of routines written in ANSI C
and organized in the form of a callable library.

GLPK supports the GNU MathProg language, which is a subset of the AMPL
language.

The GLPK package includes the following main components:

 * Revised simplex method.
 * Primal-dual interior point method.
 * Branch-and-bound method.
 * Translator for GNU MathProg.
 * Application program interface (API).
 * Stand-alone LP/MIP solver. 

%package        doc
Summary:        Documentation for %{name}

%description    doc
Documentation subpackage for %{name}.


%package devel
Summary:        Development headers and files for GLPK
Requires:       %{name}%{_isa} = %{version}-%{release}

%description devel
The glpk-devel package contains libraries and headers for developing
applications which use GLPK (GNU Linear Programming Kit).


%package utils
Summary:        GLPK-related utilities and examples
Requires:       %{name}%{_isa} = %{version}-%{release}

%description utils
The glpk-utils package contains the standalone solver program glpsol
that uses GLPK (GNU Linear Programming Kit).


%prep
%setup -q
%patch0 -p1 -b .system-suitesparse-zlib
%{__rm} -fr src/{amd,colamd,zlib}
%patch1 -p1 -b .alias

%build
export LIBS=-ldl

# Need to rebuild src/Makefile.in from src/Makefile.am
%{_bindir}/autoreconf -ifs

%configure --disable-static --with-gmp
# Get rid of undesirable hardcoded rpaths; workaround libtool reordering
# -Wl,--as-needed after all the libraries.
%{__sed} \
 -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
 -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
 -e 's|CC="\(g..\)"|CC="\1 -Wl,--as-needed"|' \
 -i libtool
%{make_build}

%install
%{makeinstall}

%check
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:%{buildroot}%{_libdir}"
%{__make} check
## Clean up directories that are included in docs
%{__rm} -rf examples/{.deps,.libs,Makefile*,glpsol,glpsol.o} doc/*.tex

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README
%license COPYING
%{_libdir}/*.so.*
%exclude %{_libdir}/*.la

%files devel
%doc ChangeLog AUTHORS NEWS
%{_includedir}/glpk.h
%{_libdir}/*.so

%files utils
%{_bindir}/*

%files doc
%doc doc examples


%changelog
* Mon Feb 05 2018 Justin Bronn <justin.bronn@radiantsolutions.com> - 4.64-1
- Initial release as Hootenanny dependency.
