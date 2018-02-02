Name:           glpk
Version:        4.61
Release:        3%{?dist}
Summary:        GNU Linear Programming Kit

License:        GPLv3+
URL:            http://www.gnu.org/software/glpk/glpk.html
Source0:        ftp://ftp.gnu.org/gnu/glpk/glpk-%{version}.tar.gz
# Un-bundle zlib (#1102855). Upstream won't accept; they want to be
# ANSI-compatible, and zlib makes POSIX assumptions.
Patch0:         %{name}-4.61-unbundle-zlib.patch
# Unbundle suitesparse
Patch1:         %{name}-4.61-unbundle-suitesparse.patch
# Fix violations of the ANSI C strict aliasing rules
Patch2:         %{name}-4.61-alias.patch

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

# This can be removed when Fedora 25 reaches EOL
Obsoletes:      %{name}-static < 4.61-1%{?dist}
Provides:       %{name}-static = %{version}-%{release}

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
%patch0 -p1 -b .system-zlib
rm -rf src/zlib
%patch1 -p1 -b .system-suitesparse
rm -fr src/{amd,colamd}
%patch2 -p1 -b .alias

%build
export LIBS=-ldl

# Need to rebuild src/Makefile.in from src/Makefile.am
autoreconf -ifs

%configure --disable-static --with-gmp
# Get rid of undesirable hardcoded rpaths; workaround libtool reordering
# -Wl,--as-needed after all the libraries.
 sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
     -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
     -e 's|CC="\(g..\)"|CC="\1 -Wl,--as-needed"|' \
     -i libtool
make %{?_smp_mflags}

%install
make install prefix=$RPM_BUILD_ROOT%{_prefix} \
	bindir=$RPM_BUILD_ROOT%{_bindir} libdir=$RPM_BUILD_ROOT%{_libdir} \
	includedir=$RPM_BUILD_ROOT%{_includedir}

%check
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$RPM_BUILD_ROOT%{_libdir}"
make check
## Clean up directories that are included in docs
rm -Rf examples/{.deps,.libs,Makefile*,glpsol,glpsol.o} doc/*.tex

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
* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.61-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.61-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr  5 2017 Jerry James <loganjerry@gmail.com> - 4.61-1
- Bump to latest upstream 4.61
- Unbundle suitesparse (amd and colamd)
- Fix aliasing issues in the minisat 1.x code
- Note that minisat 1 is bundled
- Drop the unused -static subpackage
- General spec file cleanup

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Mar 11 2016 Conrad Meyer <cemeyer@uw.edu> - 4.59-1
- Bump to latest upstream 4.59
- Update zlib-unbundling patch, context changed slightly
- Rh# 1316888

* Thu Feb 18 2016 Conrad Meyer <cemeyer@uw.edu> - 4.58-1
- Bump to latest upstream 4.58
- Update zlib-unbundling patch, context changed slightly (new simplex
  directory)
- Rh# 953012

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.55-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Conrad Meyer <cemeyer@uw.edu> - 4.55-4
- Remove tspsol from -utils subpackage description, as it is removed upstream (rh #1228966)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.55-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jan 07 2015 Conrad Meyer <cemeyer@uw.edu> - 4.55-2
- Add GMP support for better bignum performance (rh #1179702).

* Fri Aug 22 2014 Conrad Meyer <cemeyer@uw.edu> - 4.55-1
- Bump to latest upstream 4.55
- Update zlib-unbundling patch, line numbers changed slightly (new files in
  Makefile.am)
- Rhbz# 1082287

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.53-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.53-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Dan Horák <dan[at]danny.cz> - 4.53-3
- fix the zlib unbundling

* Thu May 29 2014 Cornad Meyer <cemeyer@uw.edu> - 4.53-2
- Un-bundle zlib (rh #1102855)

* Fri Feb 14 2014 Conrad Meyer <cemeyer@uw.edu> - 4.53-1
- Bump to latest upstream 4.53
- Drop glp_get_it_cnt() patch; now present in glpk.h, glpapi06.c
- Kill rpath

* Tue Oct 22 2013 Conrad Meyer <cemeyer@uw.edu> - 4.52.1-2
- Add patch to backport glp_get_it_cnt() to 4.52.1 per bug #999609

* Tue Jul 30 2013 Conrad Meyer <cemeyer@uw.edu> - 4.52.1-1
- Bump to latest upstream.

* Fri Feb 1 2013 Conrad Meyer <konrad@tylerc.org> - 4.48-1
- Bump to latest upstream.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 27 2011 Conrad Meyer <konrad@tylerc.org> - 4.47-1
- Bump to latest upstream.

* Sun Apr 24 2011 Conrad Meyer <konrad@tylerc.org> - 4.45-3
- Add %%clean section as per #696792

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 8 2010 Conrad Meyer <konrad@tylerc.org> - 4.45-1
- Bump to latest stable upstream, 4.45.

* Tue Sep 28 2010 Conrad Meyer <konrad@tylerc.org> - 4.44-1
- Bump to latest stable upstream, 4.44.

* Mon Jul 5 2010 Conrad Meyer <konrad@tylerc.org> 4.43-2
- Move header to normal includedir

* Sat Feb 20 2010 Conrad Meyer <konrad@tylerc.org> 4.43-1
- Bump to 4.43.

* Mon Feb 15 2010 Conrad Meyer <konrad@tylerc.org> 4.42-1
- Bump to 4.42.

* Tue Dec 22 2009 Conrad Meyer <konrad@tylerc.org> 4.41-1
- Bump to 4.41.

* Wed Nov 4 2009 Conrad Meyer <konrad@tylerc.org> 4.40-1
- Bump to 4.40.

* Sat Aug 8 2009 Conrad Meyer <konrad@tylerc.org> 4.39-1
- Bump to 4.39.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.36-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 27 2009 Conrad Meyer <konrad@tylerc.org> - 4.36-3
- Split out -doc subpackage.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Conrad Meyer <konrad@tylerc.org> 4.36-1
- Bump to 4.36.

* Tue Jan 27 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.35-1
- Update to 4.35.

* Fri Dec 12 2008 Conrad Meyer <konrad@tylerc.org> 4.34-1
- Update to 4.34.

* Thu Sep 25 2008 Conrad Meyer <konrad@tylerc.org> 4.31-1
- Update to 4.31.

* Tue May  6 2008 Quentin Spencer <qspencer@users.sf.net> 4.28-1
- Update to release 4.28.
- Add LIBS definition to configure step so it compiles correctly.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.25-2
- Autorebuild for GCC 4.3

* Wed Jan  2 2008 Quentin Spencer <qspencer@users.sf.net> 4.25-1
- Update to release 4.25.

* Fri Sep 14 2007 Quentin Spencer <qspencer@users.sf.net> 4.21-1
- New release. Update license tag to GPLv3.

* Thu Aug 23 2007 Quentin Spencer <qspencer@users.sf.net> 4.20-3
- Rebuild for F8.

* Thu Aug  9 2007 Quentin Spencer <qspencer@users.sf.net> 4.20-2
- Add pre and postun scripts to run ldconfig.

* Fri Jul 27 2007 Quentin Spencer <qspencer@users.sf.net> 4.20-1
- New release.
- Split static libs into separate package.

* Thu Jun 28 2007 Quentin Spencer <qspencer@users.sf.net> 4.18-1
- New release.

* Wed Mar 28 2007 Quentin Spencer <qspencer@users.sf.net> 4.15-1
- New release. Shared libraries are now supported.

* Tue Dec 12 2006 Quentin Spencer <qspencer@users.sf.net> 4.13-1
- New release.

* Tue Aug 29 2006 Quentin Spencer <qspencer@users.sf.net> 4.11-2
- Rebuild for FC6.

* Tue Jul 25 2006 Quentin Spencer <qspencer@users.sf.net> 4.11-1
- New release.

* Fri May 12 2006 Quentin Spencer <qspencer@users.sf.net> 4.10-1
- New release.

* Tue Feb 14 2006 Quentin Spencer <qspencer@users.sf.net> 4.9-2
- Add dist tag

* Tue Feb 14 2006 Quentin Spencer <qspencer@users.sf.net> 4.9-1
- New release.

* Tue Aug 09 2005 Quentin Spencer <qspencer@users.sf.net> 4.8-3
- Remove utils dependency on base package, since it doesn't exist until
  shared libraries are enabled.

* Tue Aug 09 2005 Quentin Spencer <qspencer@users.sf.net> 4.8-2
- Add -fPIC to compile flags.

* Fri Jul 22 2005 Quentin Spencer <qspencer@users.sf.net> 4.8-1
- First version.
