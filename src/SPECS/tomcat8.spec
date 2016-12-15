# To Build:
#
# sudo yum -y install rpmdevtools && rpmdev-setuptree
# rpmbuild -bb ./src/SPECS/tomcat8.spec

%define __jar_repack %{nil}
%define tomcat_group tomcat8
%define tomcat_user tomcat8
%define tomcat_home /usr/share/tomcat8
%define tomcat_user_home /var/lib/tomcat8
%define tomcat_cache_home /var/cache/tomcat8
%define tomcat_logs_home=/var/log/tomcat8
%define tomcat_config_home=/etc/tomcat8


Summary:    Apache Servlet/JSP Engine, RI for Servlet 3.1/JSP 2.3 API
Name:       tomcat8
Version:    8.5.8
BuildArch:  noarch
Release:    1
License:    Apache Software License
Group:      Networking/Daemons
URL:        http://tomcat.apache.org/
Source0:    apache-tomcat-%{version}.tar.gz
Source1:    %{name}.init
Source2:    %{name}.sysconfig
Source3:    %{name}.logrotate
Source4:    %{name}.conf
Requires:   jpackage-utils
Requires:   jdk1.8.0_111
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.

Tomcat is developed in an open and participatory environment and
released under the Apache Software License. Tomcat is intended to be
a collaboration of the best-of-breed developers from around the world.
We invite you to participate in this open development project. To
learn more about getting involved, click here.

This package contains the base tomcat installation that depends on Sun's JDK and not
on JPP packages.

%prep
%setup -q -n apache-tomcat-%{version}

%build

%install
install -d -m 755 %{buildroot}/%{tomcat_home}/
cp -R * %{buildroot}/%{tomcat_home}/

# Remove all webapps. Put webapps in /var/lib and link back.
rm -rf %{buildroot}/%{tomcat_home}/webapps
install -d -m 775 %{buildroot}%{tomcat_user_home}/webapps
cd %{buildroot}/%{tomcat_home}/
ln -s %{tomcat_user_home}/webapps webapps
chmod 775 %{buildroot}/%{tomcat_user_home}
cd -

# Remove *.bat
rm -f %{buildroot}/%{tomcat_home}/bin/*.bat

# Put logging in /var/log and link back.
rm -rf %{buildroot}/%{tomcat_home}/logs
install -d -m 755 %{buildroot}/var/log/%{name}/
cd %{buildroot}/%{tomcat_home}/
ln -s /var/log/%{name}/ logs
cd -

# Put conf in /etc/ and link back.
install -d -m 755 %{buildroot}/%{_sysconfdir}
mv %{buildroot}/%{tomcat_home}/conf %{buildroot}/%{_sysconfdir}/%{name}
cd %{buildroot}/%{tomcat_home}/
ln -s %{_sysconfdir}/%{name} conf
cd -

# Put temp and work to /var/cache and link back.
install -d -m 775 %{buildroot}%{tomcat_cache_home}
mv %{buildroot}/%{tomcat_home}/temp %{buildroot}/%{tomcat_cache_home}/
mv %{buildroot}/%{tomcat_home}/work %{buildroot}/%{tomcat_cache_home}/
cd %{buildroot}/%{tomcat_home}/
ln -s %{tomcat_cache_home}/temp
ln -s %{tomcat_cache_home}/work
chmod 775 %{buildroot}/%{tomcat_cache_home}/temp
chmod 775 %{buildroot}/%{tomcat_cache_home}/work
cd -

# Drop sbin script
install -d -m 755 %{buildroot}/%{_sbindir}
install    -m 755 %_sourcedir/%{name}.bin %{buildroot}/%{_sbindir}/%{name}

# Drop init script
install -d -m 755 %{buildroot}/%{_initrddir}
install    -m 755 %_sourcedir/%{name}.init %{buildroot}/%{_initrddir}/%{name}

# Drop conf script
install    -m 644 %_sourcedir/%{name}.conf %{buildroot}/%{_sysconfdir}/%{name}

# Drop sysconfig script
#install -d -m 755 %{buildroot}/%{_sysconfdir}/sysconfig/
#install    -m 644 %_sourcedir/%{name}.sysconfig %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

# Drop logrotate script
#install -d -m 755 %{buildroot}/%{_sysconfdir}/logrotate.d
#install    -m 644 %_sourcedir/%{name}.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

%clean
rm -rf %{buildroot}

%pre
getent group %{tomcat_group} >/dev/null || groupadd -r %{tomcat_group}
getent passwd %{tomcat_user} >/dev/null || /usr/sbin/useradd --comment "Tomcat 8 Daemon User" --shell /bin/bash -M -r -g %{tomcat_group} --home %{tomcat_home} %{tomcat_user}

%files
%defattr(-,%{tomcat_user},%{tomcat_group})
/var/log/%{name}/
%defattr(-,root,root)
%{tomcat_user_home}
%{tomcat_home}
%{_initrddir}/%{name}
%{_sbindir}/%{name}
#%{_sysconfdir}/logrotate.d/%{name}
%defattr(-,root,%{tomcat_group})
%{tomcat_cache_home}
%{tomcat_cache_home}/temp
%{tomcat_cache_home}/work
%{tomcat_user_home}/webapps
#%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*

%post
chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
  service %{name} stop > /dev/null 2>&1
  chkconfig --del %{name}
fi

%postun
if [ $1 -ge 1 ]; then
  service %{name} condrestart >/dev/null 2>&1
fi
