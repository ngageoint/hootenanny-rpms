Name:		dumb-init
Version:	%{getenv:RPMBUILD_VERSION}
Release:	%{getenv:RPMBUILD_RELEASE}%{?dist}
Summary:	Simple process supervisor and init system for containers
Group:		Applications/System
License:	MIT
URL:		https://github.com/Yelp/dumb-init
Source0:	https://github.com/Yelp/dumb-init/archive/v%{version}/dumb-init-%{version}.tar.gz

%description
dumb-init is a simple process supervisor that forwards signals to children.
It is designed to run as PID1 in minimal container environments.

%prep
%setup -q

%build
# Remove static compilation flag, as we're only targeting Enterprise Linux
# containers (like the rest of our dependencies).
%{__sed} -i -e 's/ -static//' Makefile
%{__make}

# TODO: Consider substituting hard-coded CFLAGS with `%{optflags}` in Makefile.

%install
# Placing in binary directory as it may be invoked by non-root users.
%{__install} -p -D -m 0755 dumb-init %{buildroot}%{_bindir}/dumb-init

%files
%{_bindir}/dumb-init

%changelog
* Tue Jan 16 2018 Justin Bronn <justin.bronn@digitalglobe.com> 1.2.1-1
- Initial revision.
