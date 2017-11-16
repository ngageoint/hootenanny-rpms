Name:		osmosis
Version:	0.46
Release:	1%{?dist}
Summary:	Command line Java application for processing OpenStreetMap (OSM) data

Group:		Applications/Internet
License:	Public Domain
URL:		https://github.com/openstreetmap/osmosis

BuildArch:	noarch
Requires:	java-1.8.0-openjdk

Source0:	http://bretth.dev.openstreetmap.org/osmosis-build/osmosis-%{version}.tgz
Patch1:		osmosis-fix_launcher.patch

%description
Osmosis is a command line Java application for processing OSM data.
The tool consists of pluggable components that can be chained to perform a
larger operation. For example, it has components for reading/writing
databases and files, deriving/applying changes to data sources, and sorting
data, (etc.). It has been written to easily add new features without re-writing
common tasks such as file and database handling.

Some examples of the things it can currently do are:

- Generate planet dumps from a database
- Load planet dumps into a database
- Produce change sets using database history tables
- Apply change sets to a local database
- Compare two planet dump files and produce a change set
- Re-sort the data contained in planet dump files
- Extract data inside a bounding box or polygon

Osmosis can also be included as a library in other Java applications


%files
%{_bindir}/osmosis
%{_javadir}/osmosis/*.jar
%config(noreplace) %{_sysconfdir}/osmosis/osmosis.conf
%config(noreplace) %{_sysconfdir}/osmosis/log4j.properties
%config(noreplace) %{_sysconfdir}/osmosis/plexus.conf
%{_datarootdir}/doc/%{name}-%{version}/*.txt

%prep
%setup -c -n %{name}-%{version}

%patch1 -p0 -b .fix_launcher~

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sysconfdir}/osmosis
install -d %{buildroot}%{_javadir}/osmosis
install -d %{buildroot}%{_datarootdir}/doc/%{name}-%{version}

# Osmosis binary.
install -m 0755 -D %{_builddir}/%{name}-%{version}/bin/osmosis %{buildroot}%{_bindir}/osmosis

# Java JAR files.
install -m 0644 -D %{_builddir}/%{name}-%{version}/lib/default/*.jar %{buildroot}%{_javadir}/osmosis/

# Documenation files.
install -m 0644 -D %{_builddir}/%{name}-%{version}/*.txt %{buildroot}%{_datarootdir}/doc/%{name}-%{version}/

# Configuration files.
cat > %{buildroot}%{_sysconfdir}/osmosis/osmosis.conf <<EOF
# Some examples for customization and tuning, for more visit:
#  http://wiki.openstreetmap.org/wiki/Osmosis/Tuning
#
# Use server version of JVM.
#JAVACMD_OPTIONS=-server
#
# Customize the JVM maximum heap size to 2GB.
#JAVACMD_OPTIONS=-Xmx2G
EOF
chmod 0644 %{buildroot}%{_sysconfdir}/osmosis/osmosis.conf

cat > %{buildroot}%{_sysconfdir}/osmosis/plexus.conf <<EOF
main is org.openstreetmap.osmosis.core.Osmosis from osmosis.core

[osmosis.core]
load %{_javadir}/osmosis/*.jar
EOF
chmod 0644 %{buildroot}%{_sysconfdir}/osmosis/plexus.conf

cat > %{buildroot}%{_sysconfdir}/osmosis/log4j.properties <<EOF
# Only show WARN or higher messages for org.java.plugin package
log4j.logger.org.java.plugin=WARN
EOF
chmod 0644 %{buildroot}%{_sysconfdir}/osmosis/log4j.properties

%clean

%changelog
* Tue Nov 14 2017 Justin Bronn <justin.bronn@digitalglobe.com> - 0.46-1
- Initial Release
