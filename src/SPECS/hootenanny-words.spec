Name:		hootenanny-words
Version:	1.0.0
Release:	1
Summary:	Hootenanny words dictionary
BuildArch:	noarch

%define words_filename	words1.sqlite
%define words_compress	%{words_filename}.bz2
%define deploy_dir /var/lib/hootenanny/conf
%define words_url  https://s3.amazonaws.com/hoot-rpms/support-files/%{words_compress}

Group:		Applications/Engineering
License:	GPLv3
URL:		https://github.com/ngageoint/hootenanny
Source0:	%{words_url}

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description

%prep
pwd
export BUILD_DIR=%{_builddir}/%{name}-%{version}-%{release}.%{_arch}
# Only download if the remote file is newer or a different size
wget -P %{_sourcedir} -N -nv %{words_url}
# Is there a shortcut for this?
mkdir -p $BUILD_DIR
cd $BUILD_DIR
bzcat %{_sourcedir}/%{words_compress} > %{words_filename}
/bin/chmod -Rf a+rX,u+w,g-w,o-w .

%build

%install
export BUILD_DIR=%{_builddir}/%{name}-%{version}-%{release}.%{_arch}
install -m 755 -d $RPM_BUILD_ROOT%{deploy_dir}
install -m 644 $BUILD_DIR/%{words_filename} $RPM_BUILD_ROOT%{deploy_dir}
cd $RPM_BUILD_ROOT%{deploy_dir}; ln -s %{words_filename} words.sqlite

%clean
rm -rf $RPM_BUILD_ROOT
[ -e %{_topdir}/SOURCES/%{words_compress} ] && rm %{_topdir}/SOURCES/%{words_compress}
[ -e %{_topdir}/BUILD/%{words_filename} ] && rm %{_topdir}/BUILD/%{words_filename}

%files
%{deploy_dir}/%{words_filename}
%{deploy_dir}/words.sqlite

%changelog
* Wed Feb 10 2016 Benjamin Marchant <benjamin.marchant@digitalglobe.com> - 1.0.0+
- Initial RPM creation
