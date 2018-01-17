# Enable fetch of the source by rpmbuild, as it's too big to keep in VCS.
%undefine _disable_source_fetch
%global deploy_dir %{_sharedstatedir}/hootenanny/conf
%global words_file words1.sqlite

Name:		hoot-words
Version:	1.0.0
Release:	1%{?dist}
Group:		Applications/Engineering
Summary:	Hootenanny words dictionary
License:	GPLv3
URL:		https://github.com/ngageoint/hootenanny
Source0:	https://s3.amazonaws.com/hoot-rpms/support-files/%{words_file}.bz2
BuildArch:	noarch
BuildRequires:	bzip2

%description

%prep

%build
%{_bindir}/bzcat %{SOURCE0} > %{words_file}

%install
%{__install} -m 0755 -d %{buildroot}%{deploy_dir}
%{__install} -m 0644 %{words_file} %{buildroot}%{deploy_dir}
pushd %{buildroot}%{deploy_dir}
%{__ln_s} %{words_file} words.sqlite
popd

%clean
%{__rm} -rf %{buildroot}

%files
%{deploy_dir}/%{words_file}
%{deploy_dir}/words.sqlite

%changelog
* Wed Nov 15 2017 Justin Bronn <justin.bronn@digitalglobe.com> - 1.0.0-1
- Changed package name to hoot-words.
* Wed Feb 10 2016 Benjamin Marchant <benjamin.marchant@digitalglobe.com> - 1.0.0+
- Initial RPM creation
