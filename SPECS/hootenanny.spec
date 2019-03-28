# Copyright (C) 2018 Radiant Solutions (http://www.radiantsolutions.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Required macro parameters to build a Hootenanny RPM:
#  * hoot_version_gen
#  * geos_version
#  * glpk_version
#  * gdal_version
#  * liboauthcpp_version
#  * libphonenumber_version
#  * nodejs_version
#  * stxxl_version
#  * tomcat_version

# The `hoot_version_gen` parameter allows us to automatically generate
# the version and release of the Hooteannny RPM.
%global hoot_version_tag %(echo %{hoot_version_gen} | %{__awk} -F_ '{ print $1 }')
%global hoot_extra_version %(echo %{hoot_version_gen} | %{__awk} -F_ '{ print $2 }')

# Include Hootenanny 2.x files by default.
%bcond_without hoot_ui2

# Only generate database package when requested.
%bcond_with hoot_db

%if 0%{hoot_extra_version} == 0
  # If this is a tagged release, then we want the RPM release to be
  # greater than 0 (defaults to 1).
  %{!?hoot_release: %global hoot_release 1}
  %{!?hoot_version: %global hoot_version %{hoot_version_tag}}
%else
  # If this is a development release, then create a release with
  # extra information that indicates it's a snapshot prerelease
  # of the next version.
  %global hoot_git_revision %(echo %{hoot_version_gen} | %{__awk} -F_ '{ print substr($3, 2) }')
  %global hoot_release 0.%{hoot_extra_version}.%(%{_bindir}/date -u +%%Y%%m%%d).%{hoot_git_revision}
  # Assuming the next version is the patch release + 1.
  %global hoot_version %(echo %{hoot_version_tag} | %{__awk} -F. '{ print $1 "." $2 "." ($3 + 1) }')
%endif

# Default variables for Hootenanny and Tomcat.
%{!?gdal_data: %global gdal_data %{_datadir}/gdal}
%{!?hoot_home: %global hoot_home %{_sharedstatedir}/%{name}}
%{!?tomcat_basedir: %global tomcat_basedir %{_sharedstatedir}/tomcat8}
%{!?tomcat_config: %global tomcat_config %{_sysconfdir}/tomcat8}
%{!?tomcat_home: %global tomcat_home %{_datadir}/tomcat8}
%{!?tomcat_logs: %global tomcat_logs %{_var}/log/tomcat8}
%global tomcat_version_max %(echo %{tomcat_version} | %{__awk} -F. '{ print $1 "." ($2 + 1) "." 0 }')
%global tomcat_version_min %(echo %{tomcat_version} | %{__awk} -F. '{ print $1 "." $2 "." 0 }')
%global tomcat_webapps %{tomcat_basedir}/webapps
%global services_home %{tomcat_webapps}/hoot-services

# NodeJS package includes an epoch that must be used for requirements.
%{!?nodejs_epoch: %global nodejs_epoch 1}

# Prevents services-ui from being marked that it provides GDAL.
%global __provides_exclude ^libgdal\\.so.*$

# Use explicit requirements for libgdal and libpq.
%global __requires_exclude ^lib(gdal|pq)\\.so.*$

Name:       hootenanny
Version:    %{hoot_version}
Release:    %{hoot_release}%{?dist}
Summary:    Hootenanny - we merge maps.

Group:      Applications/Engineering
License:    GPLv3
URL:        https://github.com/ngageoint/hootenanny

BuildRequires:  asciidoc
BuildRequires:  autoconf
BuildRequires:  autoconf-archive
BuildRequires:  automake
BuildRequires:  boost-devel
BuildRequires:  ccache
BuildRequires:  cppunit-devel
BuildRequires:  dblatex
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  gdb
BuildRequires:  geos-devel
BuildRequires:  git
BuildRequires:  glpk-devel
BuildRequires:  gnuplot
BuildRequires:  graphviz
BuildRequires:  hoot-gdal
BuildRequires:  hoot-gdal-devel
BuildRequires:  hoot-gdal-python
BuildRequires:  hoot-postgis24_%{pg_dotless}-devel
BuildRequires:  hoot-postgis24_%{pg_dotless}-utils
BuildRequires:  hoot-words
BuildRequires:  java-1.8.0-openjdk
BuildRequires:  libicu-devel
BuildRequires:  liboauthcpp-devel
BuildRequires:  libphonenumber-devel
BuildRequires:  libpng-devel
BuildRequires:  libpostal-devel
BuildRequires:  libxslt
BuildRequires:  log4cxx-devel
BuildRequires:  maven
BuildRequires:  nodejs-devel
BuildRequires:  opencv-devel
BuildRequires:  postgresql%{pg_dotless}-devel
BuildRequires:  proj-devel
BuildRequires:  protobuf-devel
BuildRequires:  python-argparse
BuildRequires:  python-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtbase-postgresql
BuildRequires:  stxxl-devel
BuildRequires:  texlive
BuildRequires:  texlive-collection-fontsrecommended
BuildRequires:  texlive-collection-langcyrillic
BuildRequires:  unzip
BuildRequires:  v8-devel
BuildRequires:  w3m
BuildRequires:  wget
BuildRequires:  words
BuildRequires:  zip
Source0:        %{name}-%{hoot_version_gen}.tar.gz

%description
Hootenanny was developed to provide an open source, standards-based approach to
geospatial vector data conflation. Hootenanny is designed to facilitate
automated and semi-automated conflation of critical foundation GEOINT features
in the topographic domain, namely roads (polylines), buildings (polygons), and
points-of-interest (POI's) (points). Conflation happens at the dataset level,
where the user's workflow determines the best reference dataset and source
content, geometry and attributes, to transfer to the output map.


%package core
Summary:   Hootenanny Core
Requires:  %{name}-core-deps = %{version}-%{release}
Requires:  nodejs = %{nodejs_epoch}:%{nodejs_version}
Requires:  postgresql%{pg_dotless}-libs
Group:      Applications/Engineering

%description core
Hootenanny was developed to provide an open source, standards-based approach to
geospatial vector data conflation. Hootenanny is designed to facilitate
automated and semi-automated conflation of critical foundation GEOINT features
in the topographic domain, namely roads (polylines), buildings (polygons), and
points-of-interest (POI's) (points). Conflation happens at the dataset level,
where the user's workflow determines the best reference dataset and source
content, geometry and attributes, to transfer to the output map.

This package contains the core algorithms and command line interface.


%prep
%setup -q -n %{name}-%{hoot_version_gen}


%build
source ./SetupEnv.sh

# Link in the dictionary file.
ln -s %{hoot_home}/conf/dictionary/words1.sqlite conf/dictionary/words.sqlite
ln -s %{hoot_home}/conf/dictionary/words1.sqlite conf/dictionary/words1.sqlite

# The dir configurations set the install directory to work with EL's dir structure
./configure -q --with-rnd --with-services --with-postgresql \
    --prefix=%{buildroot}%{_prefix} \
    --datarootdir=%{buildroot}%{_datarootdir}/%{name} \
    --docdir=%{buildroot}%{_docdir}/%{name} \
    --localstatedir=%{buildroot}%{hoot_home} \
    --libdir=%{buildroot}%{_libdir} \
    --sysconfdir=%{buildroot}%{_sysconfdir}

# Use ccache if it is available
%{__cp} LocalConfig.pri.orig LocalConfig.pri
command -v ccache >/dev/null 2>&1 && echo "QMAKE_CXX=ccache g++" >> LocalConfig.pri

%make_build

%{__make} ui2x-build

pushd node-export-server
npm install --production
popd


%install
# Start with $HOOT_HOME and systemd unit directories.
%{__install} -d -m 0755 %{buildroot}%{_unitdir}
%{__install} -d -m 0755 %{buildroot}%{hoot_home}

# User data directories, make directories group-writable.
%{__install} -d -m 0775 %{buildroot}%{hoot_home}/tmp
%{__install} -d -m 0775 %{buildroot}%{hoot_home}/userfiles
%{__install} -d -m 0775 %{buildroot}%{hoot_home}/userfiles/customscript
%{__install} -d -m 0775 %{buildroot}%{hoot_home}/userfiles/ingest
%{__install} -d -m 0775 %{buildroot}%{hoot_home}/userfiles/ingest/processed
%{__install} -d -m 0775 %{buildroot}%{hoot_home}/userfiles/ingest/upload
%{__install} -d -m 0775 %{buildroot}%{hoot_home}/userfiles/reports
%{__install} -d -m 0775 %{buildroot}%{hoot_home}/userfiles/tmp
%{__install} -d -m 0775 %{buildroot}%{hoot_home}/userfiles/upload

# Services (UI) files and directories.
%{__install} -d -m 0775 %{buildroot}%{tomcat_config}/conf.d
%{__install} -d -m 0775 %{buildroot}%{tomcat_home}/.deegree
%{__install} -d -m 0775 %{buildroot}%{tomcat_webapps}
%{__install} -m 0644 hoot-services/target/hoot-services*.war %{buildroot}%{tomcat_webapps}/hoot-services.war
%{__install} -d -m 0775 %{buildroot}%{tomcat_webapps}
%{__install} -d -m 0775 %{buildroot}%{tomcat_webapps}/%{name}-id
%{__install} -d -m 0775 %{buildroot}%{tomcat_webapps}/%{name}-id/data
%{__cp} -pr hoot-ui/dist/* %{buildroot}%{tomcat_webapps}/%{name}-id/
%{__install} -m 0644 hoot-ui/data/osm-plus-taginfo.csv %{buildroot}%{tomcat_webapps}/%{name}-id/data
%{__install} -m 0644 hoot-ui/data/tdsv61_field_values.json %{buildroot}%{tomcat_webapps}/%{name}-id/data
%if %{with hoot_ui2}
# Hootenanny UI 2.x files.
%{__install} -d -m 0775 %{buildroot}%{tomcat_webapps}/%{name}-id2x
%{__install} -d -m 0775 %{buildroot}%{tomcat_webapps}/%{name}-id2x/data
%{__cp} -pr hoot-ui-2x/dist/* %{buildroot}%{tomcat_webapps}/%{name}-id2x/
%{__install} -m 0644 hoot-ui/data/osm-plus-taginfo.csv %{buildroot}%{tomcat_webapps}/%{name}-id2x/data
%{__install} -m 0644 hoot-ui/data/tdsv61_field_values.json %{buildroot}%{tomcat_webapps}/%{name}-id2x/data
%endif

# Tomcat environment settings for Hootenanny.
%{__cat} >> %{buildroot}%{tomcat_config}/conf.d/hoot.conf << EOF
export GDAL_DATA=%{gdal_data}
export HOOT_HOME=%{hoot_home}
export HOOT_WORKING_NAME=%{name}
EOF

# Add a dummy Tomcat log file, `catalina.out`, to prevent error popup in UI.
%{__install} -d -m 0775 %{buildroot}%{tomcat_logs}
%{__cat} >> %{buildroot}%{tomcat_logs}/catalina.out <<EOF
Please login to the host to view the logs:

   sudo journalctl -u tomcat8
EOF

# node-export
%{__install} -d -m 0775 %{buildroot}%{hoot_home}/node-export-server
%{__cp} -p node-export-server/*.{js,json} %{buildroot}%{hoot_home}/node-export-server
%{__cp} -pr node-export-server/{node_modules,test} %{buildroot}%{hoot_home}/node-export-server
%{__cat} >> %{buildroot}%{_unitdir}/node-export.service <<EOF
[Unit]
Description=Node Export Server
After=syslog.target network.target

[Service]
Type=simple
User=tomcat
Group=tomcat
Environment='HOOT_HOME=%{hoot_home}'
WorkingDirectory=%{hoot_home}/node-export-server
ExecStart=/usr/bin/npm start
ExecStop=/usr/bin/kill -HUP \$MAINPID
Restart=on-abort

[Install]
WantedBy=multi-user.target
EOF

%if %{with hoot_db}
# Separate database package files.
%{__install} -m 0775 -d %{buildroot}%{_datadir}/hootenanny-db
%{__cp} -pr \
 hoot-services/src/main/resources/db/changelogs \
 hoot-services/src/main/resources/db/db.changelog-master.xml \
 scripts/database/blank_osmapidb.sql.in \
 %{buildroot}%{_datadir}/hootenanny-db
%endif

# install into the buildroot
%{__make} install

echo "export HOOT_HOME=%{hoot_home}" > %{buildroot}%{_sysconfdir}/profile.d/hootenanny.sh
%{__chmod} 0755 %{buildroot}%{_sysconfdir}/profile.d/hootenanny.sh

# testing files.
%{__cp} -pr test-files %{buildroot}%{hoot_home}
%{__install} -m 0775 -d %{buildroot}%{hoot_home}/test-output

%{__ln_s} %{_libdir} %{buildroot}%{hoot_home}/lib
%{__rm} %{buildroot}%{_bindir}/HootEnv.sh

# This allows all the tests to run.
%{__install} -m 0775 -d %{buildroot}%{hoot_home}/hoot-core-test/src/test
%{__ln_s} %{hoot_home}/test-files %{buildroot}%{hoot_home}/hoot-core-test/src/test/resources
%{__chmod} 0664 %{buildroot}%{hoot_home}/test-files/DcTigerRoadsHighwayExactMatchInputs.osm

# This makes it so HootEnv.sh resolves `$HOOT_HOME` properly.
%{__ln_s} %{hoot_home}/bin/HootEnv.sh %{buildroot}%{_bindir}/HootEnv.sh

# Fix the docs for the UI
%{__ln_s} %{_docdir}/%{name} %{buildroot}%{hoot_home}/docs


%check
# TODO: Determine if tests should be done here, or saved for a
#       a separate container?


%clean
%{__rm} -rf %{buildroot}


%files core
%{_includedir}/hoot
%{_libdir}/*
%docdir %{_docdir}/%{name}
%{_docdir}/%{name}
%{_bindir}/*
%config %{hoot_home}/conf/hoot.json
%{hoot_home}/bin
%{hoot_home}/conf
%{hoot_home}/docs
%{hoot_home}/hoot-core-test
%{hoot_home}/lib
%{hoot_home}/plugins
%{hoot_home}/rules
%{hoot_home}/scripts

%{hoot_home}/translations
%{_sysconfdir}/profile.d/hootenanny.sh
%{_sysconfdir}/asciidoc/filters
# No need to double-include the services WAR and the dictionary file
# already provided by hoot-words.
%exclude %{_bindir}/*.war
%exclude %{hoot_home}/conf/dictionary/words*.sqlite
# These filters will cause tests to fail.
%exclude %{_sysconfdir}/asciidoc/filters/mpl


%package services-ui
Summary:   Hootenanny UI and Services
Group:     Applications/Engineering
Requires:  %{name}-core = %{version}-%{release}
Requires:  hoot-postgis24_%{pg_dotless}
Requires:  java-1.8.0-openjdk
Requires:  liquibase
Requires:  osmosis
Requires:  postgresql%{pg_dotless}-contrib
Requires:  postgresql%{pg_dotless}-server
Requires:  tomcat8 < %{tomcat_version_max}
Requires:  tomcat8 >= %{tomcat_version_min}

%description services-ui
Hootenanny was developed to provide an open source, standards-based approach to
geospatial vector data conflation. Hootenanny is designed to facilitate
automated and semi-automated conflation of critical foundation GEOINT features
in the topographic domain, namely roads (polylines), buildings (polygons), and
points-of-interest (POI's) (points). Conflation happens at the dataset level,
where the user's workflow determines the best reference dataset and source
content, geometry and attributes, to transfer to the output map.

This package contains the UI and web services.

%files services-ui
%{_unitdir}/node-export.service

%defattr(-, root, tomcat, 0775)
%{hoot_home}/node-export-server
%{hoot_home}/test-files
%{hoot_home}/test-output
%{tomcat_config}/conf.d/hoot.conf
%{tomcat_webapps}/hoot-services.war
%{tomcat_webapps}/%{name}-id
%if %{with hoot_ui2}
%{tomcat_webapps}/%{name}-id2x
%endif

%defattr(-, tomcat, tomcat, 0775)
%{hoot_home}/tmp
%{hoot_home}/userfiles
%{tomcat_home}/.deegree
%{tomcat_logs}/catalina.out

#the order of operations during an upgrade is:
#
#    1. Run the %pre section of the RPM being installed.
#    2. Install the files that the RPM provides.
#    3. Run the %post section of the RPM.
#    4. Run the %preun of the old package.
#    5. Delete any old files not overwritten by the newer version. (This step deletes files that the new package does not require.)
#    6. Run the %postun hook of the old package.

%pre services-ui

if [ "$1" = "2" ]; then
    # Stop tomcat8 service before removing the extracted war files.
    systemctl stop tomcat8

    # Remove exploded hoot-services war remnants
    if [ -d %{services_home} ]; then
        rm -rf %{services_home}
    fi
fi

%preun services-ui

%systemd_preun node-export.service

%post services-ui

if test -f /.dockerenv; then exit 0; fi

%systemd_post node-export.service

function startTomcat() {
    local count=0
    local timeout=180
    local deploy_pattern='org\.apache\.catalina\.startup\.HostConfig\.deployWAR Deployment of web application archive \[%{tomcat_webapps}/hoot-services.war\] has finished'
    local start_time=$(date +'%%Y-%%m-%%d %%H:%%M:%%S')

    systemctl start tomcat8

    echo 'Waiting for Tomcat to start'
    while ! journalctl --since "${start_time}" -u tomcat8 | grep -q -e "${deploy_pattern}"; do
        sleep 1
        count=$(expr $count + 1)
        # Abort if we wait too long.
        if [ "$(expr ${count} \>= ${timeout})" = "1" ]; then
            echo "Timed out waiting for Tomcat to start."
            break
        fi
    done
}

function updateConfigFiles () {
    # Check for existing db config from previous install and move to right location
    if [ -f %{hoot_home}/conf/DatabaseConfigLocal.sh ]; then
        mv %{hoot_home}/conf/DatabaseConfigLocal.sh %{hoot_home}/conf/database/DatabaseConfigLocal.sh
    fi
    # Update the db password in hoot-services war
    source %{hoot_home}/conf/database/DatabaseConfig.sh

    # Configure tomcat for hoot
    # We move this here to run on install and upgrade since these commands
    # are wrapped in conditionals that allow them to skip already completed steps

    # Create Tomcat context path for tile images
    TOMCAT_SRV=%{tomcat_config}/server.xml

    # First make sure to remove the old Context entry if it exists
    sed -i '/<Context docBase=\"'${HOOT_HOME//\//\\\/}'\/ingest\/processed\" path=\"\/static\" \/>/d' $TOMCAT_SRV

    if ! grep -i --quiet 'userfiles/ingest/processed' $TOMCAT_SRV; then
        echo "Adding Tomcat context path for tile images"
        sed -i "s@<\/Host>@      <Context docBase=\""${HOOT_HOME//\//\\\/}"\/userfiles\/ingest\/processed\" path=\"\/static\" \/>\n      &@" $TOMCAT_SRV
    fi

    # Increase the Tomcat java heap size
    TOMCAT_CONF=%{tomcat_config}/tomcat8.conf
    if ! grep -i --quiet 'Xmx2048m' $TOMCAT_CONF; then
        echo "Increase the Tomcat java heap size"
        bash -c "cat >> $TOMCAT_CONF" <<EOT
#--------------
# Hoot increase java heap size
#--------------
JAVA_OPTS="$JAVA_OPTS -Xms512m -Xmx2048m"
EOT
    fi

    # Update database credentials in various locations.
    sed -i s/password\:\ hoottest/password\:\ $DB_PASSWORD/ %{services_home}/WEB-INF/classes/db/liquibase.properties
    sed -i s/DB_PASSWORD=hoottest/DB_PASSWORD=$DB_PASSWORD/ %{services_home}/WEB-INF/classes/db/db.properties
    sed -i s/password=\"hoottest\"/password=\"$DB_PASSWORD\"/ %{services_home}/META-INF/context.xml

    systemctl restart tomcat8
}

function updateLiquibase () {

    # Add hostname alias to 127.0.0.1 to avoid liquibase unknown hostname error
    if ! grep --quiet $(hostname) /etc/hosts; then
        sed -i "1 s/$/ $(hostname)/" /etc/hosts
    fi

    # Apply any database schema changes
    source %{hoot_home}/conf/database/DatabaseConfig.sh
    cd %{services_home}/WEB-INF

    # Get JDBC JAR.
    JDBC_JAR="$(ls lib/postgresql-*.jar)"

    liquibase --contexts=default,production \
        --changeLogFile=classes/db/db.changelog-master.xml \
        --promptForNonLocalDatabase=false \
        --driver=org.postgresql.Driver \
        --url=jdbc:postgresql://$DB_HOST:$DB_PORT/$DB_NAME \
        --username=$DB_USER \
        --password=$DB_PASSWORD \
        --logLevel=warning \
        --classpath=$JDBC_JAR \
        update
}

if [ "$1" = "1" ]; then
    # Perform tasks to prepare for the initial installation
    source /etc/profile.d/hootenanny.sh

    # start tomcat
    startTomcat

    # init and start postgres
    if [ ! -e /var/lib/pgsql/%{pg_version}/data/PG_VERSION ]; then
        PGSETUP_INITDB_OPTIONS="-E UTF-8 --lc-collate=en_US.UTF-8 --lc-ctype=en_US.UTF-8" \
                              /usr/pgsql-%{pg_version}/bin/postgresql%{pg_dotless}-setup initdb
    fi

    systemctl start postgresql-%{pg_version}

    while ! /usr/pgsql-%{pg_version}/bin/pg_isready; do
        echo "Waiting for postgres to start"
        sleep 1
    done

    # create Hoot services db
    if ! su -l postgres -c "psql -lqt | cut -d \| -f 1 | grep -qw hoot"; then
        RAND_PW="$(python -c "import string; from random import SystemRandom; print(''.join([SystemRandom().choice(string.ascii_letters + string.digits) for i in range(16)]))")"
        su -l postgres -c "createuser --superuser hoot || true"
        su -l postgres -c "psql -c \"ALTER USER hoot with password '${RAND_PW}';\""
        if [ -f %{hoot_home}/conf/database/DatabaseConfigDefault.sh ]; then
            echo "export DB_PASSWORD=${RAND_PW}" | tee %{hoot_home}/conf/database/DatabaseConfigLocal.sh > /dev/null
            echo "export DB_PASSWORD_OSMAPI=${RAND_PW}" | tee --append %{hoot_home}/conf/database/DatabaseConfigLocal.sh > /dev/null
            chmod a+x %{hoot_home}/conf/database/DatabaseConfigLocal.sh
        else
            sed -i s/DB_PASSWORD=.*/DB_PASSWORD=$RAND_PW/ %{hoot_home}/conf/database/DatabaseConfig.sh
        fi
        su -l postgres -c "createdb hoot --owner=hoot"
        su -l postgres -c "createdb wfsstoredb --owner=hoot"
        su -l postgres -c "psql -d hoot -c \"CREATE EXTENSION hstore;\""
        su -l postgres -c "psql -d wfsstoredb -c \"CREATE EXTENSION postgis; GRANT ALL ON geography_columns, geometry_columns, spatial_ref_sys TO PUBLIC;\""
        su -l postgres -c "psql -d postgres -c \"UPDATE pg_database SET datistemplate='true' WHERE datname='wfsstoredb';\""
    fi

    # restore saved db config file settings if present
    if [ -f %{hoot_home}/conf/database/DatabaseConfig.sh.rpmsave ]; then
        if [ -f %{hoot_home}/conf/database/DatabaseConfigDefault.sh ]; then
            grep DB_PASSWORD %{hoot_home}/conf/database/DatabaseConfig.sh.rpmsave | tee %{hoot_home}/conf/database/DatabaseConfigLocal.sh > /dev/null
            chmod a+x %{hoot_home}/conf/database/DatabaseConfigLocal.sh
        else
            mv %{hoot_home}/conf/database/DatabaseConfig.sh.rpmsave %{hoot_home}/conf/database/DatabaseConfig.sh
        fi
    fi

    # configure Postgres settings
    PG_HB_CONF=/var/lib/pgsql/%{pg_version}/data/pg_hba.conf
    if ! grep -i --quiet hoot $PG_HB_CONF; then
        sed -i '1ihost    all            hoot            127.0.0.1/32            md5' $PG_HB_CONF
        sed -i '1ihost    all            hoot            ::1/128                 md5' $PG_HB_CONF
    fi
    POSTGRES_CONF=/var/lib/pgsql/%{pg_version}/data/postgresql.conf
    if ! grep -i --quiet hoot $POSTGRES_CONF; then
        sed -i s/^max_connections/\#max_connections/ $POSTGRES_CONF
        sed -i s/^shared_buffers/\#shared_buffers/ $POSTGRES_CONF
        cat >> $POSTGRES_CONF <<EOT

#--------------
# Hoot Settings
#--------------
listen_addresses = '127.0.0.1'
max_connections = 1000
shared_buffers = 1024MB
max_files_per_process = 1000
work_mem = 16MB
maintenance_work_mem = 256MB
autovacuum = off
EOT
    fi
    systemctl restart postgresql-%{pg_version}

    # create the osm api test db
    %{hoot_home}/scripts/database/SetupOsmApiDB.sh
    rm -f /tmp/osmapidb.log

    systemctl start node-export.service

    updateConfigFiles
    updateLiquibase
elif [ "$1" = "2" ]; then
    # Perform whatever maintenance must occur after the upgrade

    # copy values from saved db config file, if present
    if [ -f %{hoot_home}/conf/database/DatabaseConfig.sh.rpmsave ]; then
        if [ -f %{hoot_home}/conf/database/DatabaseConfigDefault.sh ]; then
            grep DB_PASSWORD %{hoot_home}/conf/database/DatabaseConfig.sh.rpmsave | tee %{hoot_home}/conf/database/DatabaseConfigLocal.sh > /dev/null
            chmod a+x %{hoot_home}/conf/database/DatabaseConfigLocal.sh
        else
            mv %{hoot_home}/conf/database/DatabaseConfig.sh.rpmsave %{hoot_home}/conf/database/DatabaseConfig.sh
        fi
    fi

    source /etc/profile.d/hootenanny.sh
    source %{hoot_home}/conf/database/DatabaseConfig.sh

    startTomcat
    updateConfigFiles
    updateLiquibase
fi

%postun services-ui

if test -f /.dockerenv; then exit 0; fi

%systemd_postun node-export.service

if [ "$1" = "0" ]; then
    # Perform tasks to clean up after uninstallation

    # Stop tomcat
    systemctl stop tomcat8

    # Ensure Postgres is started
    systemctl start postgresql-%{pg_version}
    while ! /usr/pgsql-%{pg_version}/bin/pg_isready; do
        echo "Waiting for postgres to start"
        sleep 1
    done

    # Remove .deegree directory
    if [ -d %{tomcat_home}/.deegree ]; then
        rm -rf %{tomcat_home}/.deegree
    fi

    # Remove exploded hoot-services war remnants
    if [ -d %{services_home} ]; then
        rm -rf %{services_home}
    fi

    systemctl start tomcat8
fi


%package   autostart
Summary:   Hootenanny Autostart
Requires:  %{name}-services-ui = %{version}-%{release}
Group:     Applications/Engineering
BuildArch: noarch

%description autostart
Hootenanny was developed to provide an open source, standards-based approach to
geospatial vector data conflation. Hootenanny is designed to facilitate
automated and semi-automated conflation of critical foundation GEOINT features
in the topographic domain, namely roads (polylines), buildings (polygons), and
points-of-interest (POI's) (points). Conflation happens at the dataset level,
where the user's workflow determines the best reference dataset and source
content, geometry and attributes, to transfer to the output map.

This package sets the PostgreSQL and Tomcat and NodeJS services to autostart
to run Hootenanny.

%files autostart

%post autostart

if test -f /.dockerenv; then exit 0; fi

if [ "$1" = "1" ]; then
    # set Postgres to autostart
    systemctl enable postgresql-%{pg_version}
    # set Tomcat to autostart
    systemctl enable tomcat8
    # set NodeJS node-export-server to autostart
    systemctl enable node-export
fi



%postun autostart

if test -f /.dockerenv; then exit 0; fi

if [ "$1" = "0" ]; then
    # set Postgres to NOT autostart
    systemctl disable postgresql-%{pg_version}
    # set Tomcat to NOT autostart
    systemctl disable tomcat8
    # set NodeJS node-export-server to NOT autostart
    systemctl disable node-export
fi


%package services-devel-deps
Summary:   Development dependencies for Hootenanny Services
Group:     Development/Libraries
BuildArch: noarch
Requires:  %{name}-core-devel-deps = %{version}-%{release}
Requires:  hoot-postgis24_%{pg_dotless}
Requires:  hoot-postgis24_%{pg_dotless}-utils
Requires:  liquibase
Requires:  maven
Requires:  nodejs-devel = %{nodejs_epoch}:%{nodejs_version}
Requires:  postgresql%{pg_dotless}-devel
Requires:  postgresql%{pg_dotless}-server
Requires:  postgresql%{pg_dotless}-contrib

%description services-devel-deps
Hootenanny was developed to provide an open source, standards-based approach to
geospatial vector data conflation. Hootenanny is designed to facilitate
automated and semi-automated conflation of critical foundation GEOINT features
in the topographic domain, namely roads (polylines), buildings (polygons), and
points-of-interest (POI's) (points). Conflation happens at the dataset level,
where the user's workflow determines the best reference dataset and source
content, geometry and attributes, to transfer to the output map.

This packages contains the dependencies to build and develop the Hootenanny
services. Use this if you want to build and test from github.

%files services-devel-deps

%post services-devel-deps

if test -f /.dockerenv; then exit 0; fi

if [ "$1" = "1" ]; then
    # Perform tasks to prepare for the initial installation

    # init and start postgres
    if [ ! -e /var/lib/pgsql/%{pg_version}/data/PG_VERSION ]; then
        PGSETUP_INITDB_OPTIONS="-E UTF-8 --lc-collate=en_US.UTF-8 --lc-ctype=en_US.UTF-8" \
                              /usr/pgsql-%{pg_version}/bin/postgresql%{pg_dotless}-setup initdb
    fi

    systemctl start postgresql-%{pg_version}

    while ! /usr/pgsql-%{pg_version}/bin/pg_isready; do
        echo "Waiting for postgres to start"
        sleep 1
    done

    # create Hoot services db
    if ! su -l postgres -c "psql -lqt | cut -d \| -f 1 | grep -qw hoot"; then
        su -l postgres -c "createuser --superuser hoot || true"
        su -l postgres -c "psql -c \"ALTER USER hoot WITH PASSWORD 'hoottest';\""
        su -l postgres -c "createdb hoot --owner=hoot"
        su -l postgres -c "createdb wfsstoredb --owner=hoot"
        su -l postgres -c "psql -d hoot -c \"CREATE EXTENSION hstore;\""
        su -l postgres -c "psql -d wfsstoredb -c \"CREATE EXTENSION postgis; GRANT ALL ON geography_columns, geometry_columns, spatial_ref_sys TO PUBLIC;\""
        su -l postgres -c "psql -d postgres -c \"UPDATE pg_database SET datistemplate='true' WHERE datname='wfsstoredb'\";"
    fi

    # configure Postgres settings
    PG_HB_CONF=/var/lib/pgsql/%{pg_version}/data/pg_hba.conf
    if ! grep -i --quiet hoot $PG_HB_CONF; then
        sed -i '1ihost    all            hoot            127.0.0.1/32            md5' $PG_HB_CONF
        sed -i '1ihost    all            hoot            ::1/128                 md5' $PG_HB_CONF
    fi
    POSTGRES_CONF=/var/lib/pgsql/%{pg_version}/data/postgresql.conf
    if ! grep -i --quiet HOOT $POSTGRES_CONF; then
        sed -i s/^max_connections/\#max_connections/ $POSTGRES_CONF
        sed -i s/^shared_buffers/\#shared_buffers/ $POSTGRES_CONF
        cat >> $POSTGRES_CONF <<EOT

#--------------
# Hoot Settings
#--------------
listen_addresses = '127.0.0.1'
max_connections = 1000
shared_buffers = 1024MB
max_files_per_process = 1000
work_mem = 16MB
maintenance_work_mem = 256MB
autovacuum = off
EOT
    fi
    systemctl restart postgresql-%{pg_version}
fi

%postun services-devel-deps

if test -f /.dockerenv; then exit 0; fi

if [ "$1" = "0" ]; then
    # Perform tasks to clean up after uninstallation

    # Ensure Postgres is started
    systemctl start postgresql-%{pg_version}
    while ! /usr/pgsql-%{pg_version}/bin/pg_isready; do
        echo "Waiting for postgres to start"
        sleep 1
    done
fi


%package core-devel-deps
Summary:   Development dependencies for Hootenanny Core
Group:     Development/Libraries
BuildArch: noarch
Requires:  %{name}-core-deps = %{version}-%{release}
Requires:  autoconf
Requires:  automake
Requires:  boost-devel
Requires:  cppunit-devel
Requires:  gcc-c++
Requires:  gdb
Requires:  geos-devel = %{geos_version}
Requires:  git
Requires:  glpk-devel = %{glpk_version}
Requires:  hoot-words
Requires:  libicu-devel
Requires:  log4cxx-devel
Requires:  nodejs-devel = %{nodejs_epoch}:%{nodejs_version}
Requires:  opencv-devel
Requires:  postgresql%{pg_dotless}-devel
Requires:  proj-devel
Requires:  protobuf-devel
Requires:  python-argparse
Requires:  python-devel
Requires:  qt5-qtbase-devel
Requires:  stxxl-devel = %{stxxl_version}
Requires:  v8-devel
# Documentation and report-related dependencies.
Requires:  doxygen
Requires:  liberation-fonts-common
Requires:  liberation-sans-fonts
Requires:  libxslt
Requires:  texlive
Requires:  texlive-collection-fontsrecommended
Requires:  texlive-collection-langcyrillic

%description core-devel-deps
Hootenanny was developed to provide an open source, standards-based approach to
geospatial vector data conflation. Hootenanny is designed to facilitate
automated and semi-automated conflation of critical foundation GEOINT features
in the topographic domain, namely roads (polylines), buildings (polygons), and
points-of-interest (POI's) (points). Conflation happens at the dataset level,
where the user's workflow determines the best reference dataset and source
content, geometry and attributes, to transfer to the output map.

This packages contains the dependencies to build and develop the Hootenanny
core. Use this if you want to build from github.

%files core-devel-deps


%package core-deps
Summary:   Dependencies for Hootenanny Core
Group:     Development/Libraries
BuildArch: noarch
Requires:  boost-iostreams
Requires:  boost-system
Requires:  cppunit
Requires:  FileGDBAPI
Requires:  geos = %{geos_version}
Requires:  glpk = %{glpk_version}
Requires:  hoot-gdal = %{gdal_version}
Requires:  hoot-gdal-devel = %{gdal_version}
Requires:  hoot-gdal-python = %{gdal_version}
Requires:  hoot-words
Requires:  libicu
Requires:  liboauthcpp = %{liboauthcpp_version}
Requires:  libphonenumber = %{libphonenumber_version}
Requires:  libpostal
Requires:  libpostal-data
Requires:  log4cxx
Requires:  nodejs = %{nodejs_epoch}:%{nodejs_version}
Requires:  opencv
Requires:  postgresql%{pg_dotless}-libs
Requires:  protobuf
Requires:  python-matplotlib
Requires:  qt5-qtbase
Requires:  qt5-qtbase-postgresql
Requires:  qt5-qtx11extras
Requires:  stxxl = %{stxxl_version}
Requires:  unzip
Requires:  v8
Requires:  wget
Requires:  words
Requires:  zip

%description core-deps
Hootenanny was developed to provide an open source, standards-based approach to
geospatial vector data conflation. Hootenanny is designed to facilitate
automated and semi-automated conflation of critical foundation GEOINT features
in the topographic domain, namely roads (polylines), buildings (polygons), and
points-of-interest (POI's) (points). Conflation happens at the dataset level,
where the user's workflow determines the best reference dataset and source
content, geometry and attributes, to transfer to the output map.

This packages contains the dependencies to run the Hootenanny core.

%files core-deps

%if %{with hoot_db}
%package   db
Summary:   Hootenanny Database Server Files
Group:     Applications/Engineering
BuildArch: noarch

%description db
Database-related files for use by servers that do not need the entire
Hootenanny stack.

%files db
%{_datadir}/hootenanny-db
%endif

%changelog
* Tue Jan 30 2018 Justin Bronn <justin.bronn@radiantsolutions.com> - 0.2.38-1
- Initial CentOS 7 release.

* Wed Nov 08 2017 Matt Jackson <matthew.jackson@digitalglobe.com> - 0.2.36+
- Many Centos7 fixes

* Fri May 12 2017 Matt Jackson <matthew.jackson@digitalglobe.com> - 0.2.33+
- Fix libpq issues

* Wed Feb 22 2017 Brandon Witham <brandon.witham@digitalglobe.com> - 0.2.32+
- hoot #1415 changes

* Thu Feb 09 2017 Ben Marchant <benjamin.marchant@digitalglobe.com> - 0.2.32+
- GDAL 2.1.3 upgrade

* Wed Dec 21 2016 Dmitriy Mylov <dmitriy.mylov@digitalglobe.com>
- Oracle Java 8 and Tomcat 8.5.8 upgrades

* Tue Aug 30 2016 Matt Jackson <matthew.jackson@digitalglobe.com> - 0.2.23+
- Added symlink for hootenanny docs so they are available in the UI

* Thu Feb 25 2016 Brian Hatchl <brian.hatchl@digitalglobe.com> - 0.2.23+
- Adding ui-services and autostart packages

* Fri Jan 29 2016 Ben Marchant <benjamin.marchant@digitalglobe.com> - 0.2.21+
- Adding stxxl and stxxl-devel

* Thu Jan 21 2016 Jason R. Surratt <jason.surratt@digitalglobe.com> - 0.2.21+
- Initial attempt
