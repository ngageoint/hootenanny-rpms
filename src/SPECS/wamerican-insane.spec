Name:		wamerican-insane
Version:	7.1
Release:	1%{?dist}
Summary:	American English dictionary words for /usr/share/dict

Group:		System Environment/Libraries
License:	Public Domain
URL:		http://wordlist.aspell.net

BuildArch:	noarch

Source0:	wamerican-insane-%{version}.tar.xz

%description
This package provides the file /usr/share/dict/american-english-insane
containing a list of English words with American spellings.
This list can be used by spelling checkers, and by programs such
as look(1).  Adapted from Ubuntu package of the same name.

%files
%{_datarootdir}/doc/%{name}-%{version}/copyright
%{_datarootdir}/dict/american-english-insane
%{_mandir}/man5/american-english-insane.5.gz

%prep
mkdir -p %{name}-%{version}
tar -C %{name}-%{version} -xf %{SOURCE0}

%build
true

%install
install -d -m 0755 %{buildroot}%{_datarootdir}/dict
install -d -m 0755 %{buildroot}%{_datarootdir}/doc/%{name}-%{version}
install -d -m 0755 %{buildroot}%{_mandir}/man5
install -p -m 0644 -D %{_builddir}/%{name}-%{version}%{_datarootdir}/dict/american-english-insane %{buildroot}%{_datarootdir}/dict/american-english-insane
install -p -m 0644 -D %{_builddir}/%{name}-%{version}%{_datarootdir}/doc/wamerican-insane/copyright %{buildroot}%{_datarootdir}/doc/%{name}-%{version}/copyright
install -p -m 0644 -D %{_builddir}/%{name}-%{version}%{_mandir}/man5/american-english-insane.5.gz %{buildroot}%{_mandir}/man5/american-english-insane.5.gz

%check

%clean

%changelog
* Tue Nov 14 2017 Justin Bronn <justin.bronn@digitalglobe.com> - 7.1-1
- Initial Release
