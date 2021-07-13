Name: lcov
Version: %{rpmbuild_version}
Release: %{rpmbuild_release}%{?dist}

Summary: LTP GCOV extension code coverage tool
License: GPLv2+

URL: https://github.com/linux-test-project/lcov/
Source0: https://github.com/linux-test-project/lcov/releases/download/v%{version}/lcov-%{version}.tar.gz

BuildArch: noarch
BuildRequires: perl-generators
BuildRequires: git-core
BuildRequires: make

Requires: /usr/bin/gcov
Requires: /usr/bin/find
Requires: perl(GD::Image)

%description
LCOV is an extension of GCOV, a GNU tool which provides information
about what parts of a program are actually executed (i.e. "covered")
while running a particular test case. The extension consists of a set
of PERL scripts which build on the textual GCOV output to implement
HTML output and support for large projects.

%prep
%autosetup -S git_am

%install
make install DESTDIR=$RPM_BUILD_ROOT BIN_DIR=%{_bindir} MAN_DIR=%{_mandir} CFG_DIR=%{_sysconfdir}

%files
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/lcovrc

%changelog
* Mon Jul 12 2021 Justin Bronn <justin.bronn@maxar.com> 1.15-1
- Initial revision.
