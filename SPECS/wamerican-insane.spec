Name:		wamerican-insane
Version:	%{rpmbuild_version}
Release:	%{rpmbuild_release}%{?dist}
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
%setup -c -n %{name}-%{version}

%build

%install
%{__install} -d -m 0755 %{buildroot}%{_datarootdir}/dict
%{__install} -d -m 0755 %{buildroot}%{_datarootdir}/doc/%{name}-%{version}
%{__install} -d -m 0755 %{buildroot}%{_mandir}/man5
%{__install} -p -m 0644 -D .%{_datarootdir}/dict/american-english-insane %{buildroot}%{_datarootdir}/dict/american-english-insane
%{__install} -p -m 0644 -D .%{_datarootdir}/doc/wamerican-insane/copyright %{buildroot}%{_datarootdir}/doc/%{name}-%{version}/copyright
%{__install} -p -m 0644 -D .%{_mandir}/man5/american-english-insane.5.gz %{buildroot}%{_mandir}/man5/american-english-insane.5.gz

%check

%clean

%changelog
* Tue Nov 14 2017 Justin Bronn <justin.bronn@digitalglobe.com> - 7.1-1
- Initial Release
