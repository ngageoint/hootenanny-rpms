Name:		hootenanny-words
Version:	1.0.0
Release:	1%{?dist}
Summary:	Hootenanny words dictionary
BuildArch:	noarch

%define words_filename	words1.sqlite
%define deploy_dir /var/lib/hootenanny/conf
%define words_url  https://github.com/ngageoint/hootenanny/releases/download/v0.2.16/%{words_filename}

Group:		Applications/Engineering
License:	GPLv3
URL:		https://github.com/ngageoint/hootenanny
Source0:	%{words_url}

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description

%prep
cd %{_topdir}/SOURCES
[ -e %{words_filename} ] && rm %{words_filename}
wget -nv %{words_url}
cd %{_topdir}/BUILD
cp %{_topdir}/SOURCES/%{words_filename} ./
/bin/chmod -Rf a+rX,u+w,g-w,o-w .

%build

%install
install -m 755 -d $RPM_BUILD_ROOT%{deploy_dir}
install -m 644 %{words_filename} $RPM_BUILD_ROOT%{deploy_dir}
cd $RPM_BUILD_ROOT%{deploy_dir}; ln -s %{words_filename} words.sqlite

%clean
rm -rf $RPM_BUILD_ROOT
[ -e %{_topdir}/SOURCES/%{words_filename} ] && rm %{_topdir}/SOURCES/%{words_filename}
[ -e %{_topdir}/BUILD/%{words_filename} ] && rm %{_topdir}/BUILD/%{words_filename}

%files
%{deploy_dir}/%{words_filename}
%{deploy_dir}/words.sqlite

%changelog
* Wed Feb 10 2016 Benjamin Marchant <benjamin.marchant@digitalglobe.com> - 1.0.0+
- Initial RPM creation
