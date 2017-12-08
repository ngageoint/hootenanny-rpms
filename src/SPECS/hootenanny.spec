Name:       hootenanny
Version:    %{hoot_version}
Release:    %{hoot_release}%{?dist}
Summary:    Hootenanny - we merge maps.

Group:      Applications/Engineering
License:    GPLv3
URL:        https://github.com/ngageoint/hootenanny

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  boost-devel
BuildRequires:  cppunit-devel
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  gdb
BuildRequires:  geos-devel >= %{geos_min_version}
BuildRequires:  git
BuildRequires:  glpk-devel
BuildRequires:  graphviz
BuildRequires:  hoot-gdal-devel >= %{gdal_min_version}
BuildRequires:  hoot-gdal-python >= %{gdal_min_version}
BuildRequires:  hoot-words >= 1.0.0
BuildRequires:  java-1.8.0-openjdk
BuildRequires:  libicu-devel
BuildRequires:  libspatialite-devel
BuildRequires:  libxslt
BuildRequires:  log4cxx-devel
BuildRequires:  nodejs-devel
BuildRequires:  opencv-devel
BuildRequires:  postgresql%{pg_dotless}-devel
BuildRequires:  proj-devel
BuildRequires:  protobuf-devel
BuildRequires:  python-argparse
BuildRequires:  python-devel
BuildRequires:  qt-devel
BuildRequires:  texlive
BuildRequires:  gnuplot
BuildRequires:  unzip
BuildRequires:  v8-devel
BuildRequires:  w3m
BuildRequires:  wget
BuildRequires:  words
BuildRequires:  zip

Source0:        %{name}-%{version}.tar.gz

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
Requires:  postgresql%{pg_dotless}-libs
%global __requires_exclude ^libpq\\.so
Requires:  %{name}-core-deps = %{version}-%{release}


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
%setup -q -n %{name}-%{version}

%build
source ./SetupEnv.sh

# Sort out the postgres version. We can't rely on having pg_config in our path
PG_VERSION=$(psql --version | egrep -o '[0-9]{1,}\.[0-9]{1,}')


# The dir configurations set the install directory to work with EL's dir structure
# aclocal && autoconf && autoheader && automake --add-missing --copy && \

./configure -q --with-rnd --with-services \
    --with-postgresql=/usr/pgsql-%{pg_version}/bin/pg_config      \
    --prefix=$RPM_BUILD_ROOT/usr/ \
    --datarootdir=$RPM_BUILD_ROOT/usr/share/hootenanny/ \
    --docdir=$RPM_BUILD_ROOT/usr/share/doc/hootenanny/ \
    --localstatedir=$RPM_BUILD_ROOT/var/lib/hootenanny/ \
    --libdir=$RPM_BUILD_ROOT/usr/lib64 \
    --sysconfdir=$RPM_BUILD_ROOT/etc/

# Use ccache if it is available
cp LocalConfig.pri.orig LocalConfig.pri
command -v ccache >/dev/null 2>&1 && echo "QMAKE_CXX=ccache g++" >> LocalConfig.pri

make -s %{?_smp_mflags}

# This may be causing failure due to node-mapnik dependency on
# Requires: libc.so.6(GLIBC_2.14)(64bit)
cd node-mapnik-server
npm install --production

cd node-export-server
npm install --production

%install

# UI stuff
mkdir -p $RPM_BUILD_ROOT/var/lib/tomcat8/webapps
cp hoot-services/target/hoot-services*.war $RPM_BUILD_ROOT/var/lib/tomcat8/webapps/hoot-services.war
cp -R hoot-ui/dist $RPM_BUILD_ROOT/var/lib/tomcat8/webapps/hootenanny-id
mkdir -p $RPM_BUILD_ROOT/var/lib/tomcat8/webapps/hootenanny-id/data
cp hoot-ui/data/osm-plus-taginfo.csv $RPM_BUILD_ROOT/var/lib/tomcat8/webapps/hootenanny-id/data
cp hoot-ui/data/tdsv61_field_values.json $RPM_BUILD_ROOT/var/lib/tomcat8/webapps/hootenanny-id/data
mkdir -p $RPM_BUILD_ROOT/etc/systemd
cp node-mapnik-server/systemd/node-mapnik.service $RPM_BUILD_ROOT/etc/systemd/system/node-mapnik.service
cp node-export-server/systemd/node-export.service $RPM_BUILD_ROOT/etc/systemd/system/node-export.service
mkdir -p $RPM_BUILD_ROOT/var/lib/hootenanny
cp -R node-mapnik-server/ $RPM_BUILD_ROOT/var/lib/hootenanny/node-mapnik-server
cp -R node-export-server/ $RPM_BUILD_ROOT/var/lib/hootenanny/node-export-server

make install
echo "export HOOT_HOME=/var/lib/hootenanny" > $RPM_BUILD_ROOT/etc/profile.d/hootenanny.sh

chmod 755 $RPM_BUILD_ROOT/etc/profile.d/hootenanny.sh
cp -R test-files/ $RPM_BUILD_ROOT/var/lib/hootenanny/
ln -s /usr/lib64 $RPM_BUILD_ROOT/var/lib/hootenanny/lib
rm $RPM_BUILD_ROOT/usr/bin/HootEnv.sh
# This allows all the tests to run.
mkdir -p $RPM_BUILD_ROOT/var/lib/hootenanny/hoot-core-test/src/test/
ln -s /var/lib/hootenanny/test-files/ $RPM_BUILD_ROOT/var/lib/hootenanny/hoot-core-test/src/test/resources
# This makes it so HootEnv.sh resolves hoot home properly.
ln -s /var/lib/hootenanny/bin/HootEnv.sh $RPM_BUILD_ROOT/usr/bin/HootEnv.sh
# Fix the docs for the UI
ln -s /usr/share/doc/hootenanny  $RPM_BUILD_ROOT/var/lib/hootenanny/docs


%check
source ./SetupEnv.sh
# The excluded tests are failing on CentOS now and waiting on a fix
# HootTest --exclude=.*RubberSheetConflateTest.sh \
HootTest --slow --diff

cd hoot-services
make test -s

%clean
rm -rf %{buildroot}

%files core
%{_includedir}/hoot
%{_libdir}/*
%docdir /usr/share/doc/%{name}
%{_datarootdir}/doc/%{name}
%{_bindir}/*
%config %{_sharedstatedir}/%{name}/conf/hoot.json
%{_sharedstatedir}/%{name}
%{_sysconfdir}/profile.d/hootenanny.sh
%{_sysconfdir}/asciidoc/filters/


%package services-ui
Summary:   Hootenanny UI and Services
Requires:  tomcat8
Requires:  %{name}-core = %{version}-%{release}
Requires:  postgresql%{pg_dotless}-server
Requires:  postgresql%{pg_dotless}-contrib
Requires:  hoot-postgis
Requires:  java-1.8.0-openjdk
Requires:  liquibase
Requires:  npm
Requires:  pwgen
Group:     Applications/Engineering

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
%attr(755, tomcat, tomcat) %{_sharedstatedir}/tomcat8/webapps/hoot-services.war
%attr(755, tomcat, tomcat) %{_sharedstatedir}/tomcat8/webapps/hootenanny-id
/etc/init.d/node-mapnik-server
/etc/init.d/node-export-server

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
    # Perform whatever maintenance must occur before the upgrade

    # Remove exploded hoot-services war remnants
    SERVICES_HOME=/var/lib/tomcat8/webapps/hoot-services
    if [ -d $SERVICES_HOME ]; then
        sudo rm -rf $SERVICES_HOME
    fi
fi

%post services-ui
function updateConfigFiles () {
    # Check for existing db config from previous install and move to right location
    if [ -f /var/lib/hootenanny/conf/DatabaseConfigLocal.sh ]; then
        mv /var/lib/hootenanny/conf/DatabaseConfigLocal.sh /var/lib/hootenanny/conf/database/DatabaseConfigLocal.sh
    fi
    # Update the db password in hoot-services war
    source /var/lib/hootenanny/conf/database/DatabaseConfig.sh

    # Fix gdal2tiles path (can be removed once reference fixed in hoot code)
    if [ ! -h /usr/local/bin/gdal2tiles.py ]; then
        ln -s /usr/bin/gdal2tiles.py /usr/local/bin/gdal2tiles.py
    fi

    # Configure tomcat for hoot
    # We move this here to run on install and upgrade since these commands
    # are wrapped in conditionals that allow them to skip already completed steps

    # Create Tomcat context path for tile images
    TOMCAT_SRV=/etc/tomcat8/server.xml

    # First make sure to remove the old Context entry if it exists
    sudo sed -i '/<Context docBase=\"\/var\/lib\/hootenanny\/ingest\/processed\" path=\"\/static\" \/>/d' $TOMCAT_SRV

    if ! grep -i --quiet 'userfiles/ingest/processed' $TOMCAT_SRV; then
        echo "Adding Tomcat context path for tile images"
        sudo sed -i "s@<\/Host>@      <Context docBase=\"\/var\/lib\/hootenanny\/userfiles\/ingest\/processed\" path=\"\/static\" \/>\n      &@" $TOMCAT_SRV
    fi

    # Allow linking in Tomcat context
    TOMCAT_CTX=/etc/tomcat8/context.xml

    # First, fix potential pre-existing setting of 'allowLinking' that doesn't work on tomcat8
    sudo sed -i "s@^<Context allowLinking=\"true\">@<Context>@" $TOMCAT_CTX

    # Now, set allowLinking if needed
    if ! grep -i --quiet 'allowLinking="true"' $TOMCAT_CTX; then
        echo "Set allowLinking to true in Tomcat context"
        sudo sed -i "/<Context>/a \    <Resources allowLinking=\"true\" />" $TOMCAT_CTX
    fi

    # Increase the Tomcat java heap size
    TOMCAT_CONF=/etc/tomcat8/tomcat8.conf
    if ! grep -i --quiet 'Xmx2048m' $TOMCAT_CONF; then
        echo "Increase the Tomcat java heap size"
        sudo bash -c "cat >> $TOMCAT_CONF" <<EOT
#--------------
# Hoot increase java heap size
#--------------
JAVA_OPTS="$JAVA_OPTS -Xms512m -Xmx2048m"

EOT
    fi

    # Create directories for webapp
    TOMCAT_HOME=/usr/share/tomcat8
    if [ ! -d $TOMCAT_HOME/.deegree ]; then
        echo "Creating .deegree directory for webapp"
        sudo mkdir $TOMCAT_HOME/.deegree
        sudo chown tomcat:tomcat $TOMCAT_HOME/.deegree
    fi

    # Directory that now hosts several folders used by the Services code.
    USER_FILES_HOME=/var/lib/hootenanny/userfiles
    if [ ! -d $USER_FILES_HOME ]; then
        echo "Creating userfiles directory"
        sudo mkdir -p $USER_FILES_HOME
    fi

    # Tomcat needs this directory to exist for the server to start.
    # Tomcat's server.xml has a docBase reference to this folder.
    BASEMAP_UPLOAD_HOME=$USER_FILES_HOME/ingest/upload
    if [ ! -d $BASEMAP_UPLOAD_HOME ]; then
        echo "Creating $BASEMAP_UPLOAD_HOME directory"
        sudo mkdir -p $BASEMAP_UPLOAD_HOME
    fi

    migrateFiles

    # make sure everything undedr $HOOT_HOME/userfiles is owned by tomcat:tomcat
    sudo chown -R tomcat:tomcat $HOOT_HOME/userfiles

    sudo service tomcat8 restart

    while [ ! -f /var/lib/tomcat8/webapps/hoot-services/WEB-INF/classes/db/db.properties ]; do
        echo "Waiting for hoot-services.war to deploy"
        sleep 1
    done

    sudo sed -i s/password\:\ hoottest/password\:\ $DB_PASSWORD/ /var/lib/tomcat8/webapps/hoot-services/WEB-INF/classes/db/liquibase.properties
    sudo sed -i s/DB_PASSWORD=hoottest/DB_PASSWORD=$DB_PASSWORD/ /var/lib/tomcat8/webapps/hoot-services/WEB-INF/classes/db/db.properties
    sudo sed -i s/\<Password\>hoottest\<\\/Password\>/\<Password\>$DB_PASSWORD\<\\/Password\>/ /var/lib/tomcat8/webapps/hoot-services/WEB-INF/workspace/jdbc/WFS_Connection.xml

    # make sure tomcat is using correct Java
    sudo sed -i '/.*JAVA_HOME=.*/c\JAVA_HOME=\/usr\/java\/jdk1.8.0_144' /etc/tomcat8/tomcat8.conf

    sudo service tomcat8 restart
}

function migrateFiles() {
    if [ ! -d "$HOOT_HOME/userfiles/ingest/processed" ]; then
        mkdir -p $HOOT_HOME/userfiles/ingest/processed
    fi

    # tmp and upload will now reside under $HOOT_HOME/userfiles/
    # The folders will be automatically created under $HOOT_HOME/userfiles by hoot-services webapp during Tomcat startup
    rm -rf $HOOT_HOME/upload
    rm -rf $HOOT_HOME/tmp

    if [ -d "$HOOT_HOME/data/reports" ]; then
        echo "Moving contents of $HOOT_HOME/data/reports to $HOOT_HOME/userfiles/"
        cp -R $HOOT_HOME/data/reports $HOOT_HOME/userfiles/
        rm -rf $HOOT_HOME/data/reports
    fi

    if [ -d "$HOOT_HOME/customscript" ]; then
        echo "Moving contents of $HOOT_HOME/customscript to $HOOT_HOME/userfiles/"
        cp -R $HOOT_HOME/customscript $HOOT_HOME/userfiles/
        rm -rf $HOOT_HOME/customscript
    fi

    if [ -d "$HOOT_HOME/ingest" ]; then
        echo "Moving contents of $HOOT_HOME/ingest to $HOOT_HOME/userfiles/"
        cp -R $HOOT_HOME/ingest $HOOT_HOME/userfiles/
        rm -rf $HOOT_HOME/ingest
    fi

    rm -rf $HOOT_HOME/data

    # Always start with a clean $HOOT_HOME/userfiles/tmp
    rm -rf $HOOT_HOME/userfiles/tmp
}

function updateLiquibase () {

    # Add hostname alias to 127.0.0.1 to avoid liquibase unknown hostname error
    if ! grep --quiet $(hostname) /etc/hosts; then
        sudo sed -i "1 s/$/ $(hostname)/" /etc/hosts
    fi

    # Apply any database schema changes
    source /var/lib/hootenanny/conf/database/DatabaseConfig.sh
    TOMCAT_HOME=/usr/share/tomcat8
    source /var/lib/hootenanny/conf/database/DatabaseConfig.sh
    cd $TOMCAT_HOME/webapps/hoot-services/WEB-INF
    liquibase --contexts=default,production \
        --changeLogFile=classes/db/db.changelog-master.xml \
        --promptForNonLocalDatabase=false \
        --driver=org.postgresql.Driver \
        --url=jdbc:postgresql://$DB_HOST:$DB_PORT/$DB_NAME \
        --username=$DB_USER \
        --password=$DB_PASSWORD \
        --logLevel=warning \
        --classpath=lib/postgresql-9.4.1208.jre7.jar \
        update
}

if [ "$1" = "1" ]; then
    # Perform tasks to prepare for the initial installation
    source /etc/profile.d/hootenanny.sh

    # init and start Postgres
    PG_SERVICE=$(ls /etc/init.d | grep postgresql- | sort | tail -1)
    sudo service $PG_SERVICE initdb
    sudo service $PG_SERVICE start
    while ! PG_VERSION=$(sudo -u postgres psql -c 'SHOW SERVER_VERSION;' | egrep -o '[0-9]{1,}\.[0-9]{1,}'); do
        echo "Waiting for postgres to start"
        sleep 1
    done

    sudo service tomcat8 start

    # create Hoot services db
    if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw hoot; then
        RAND_PW=$(pwgen -s 16 1)
        sudo -u postgres createuser --superuser hoot || true
        sudo -u postgres psql -c "alter user hoot with password '$RAND_PW';"
        if [ -f /var/lib/hootenanny/conf/database/DatabaseConfigDefault.sh ]; then
            echo "export DB_PASSWORD=$RAND_PW" | sudo tee /var/lib/hootenanny/conf/database/DatabaseConfigLocal.sh > /dev/null
            echo "export DB_PASSWORD_OSMAPI=$RAND_PW" | sudo tee --append /var/lib/hootenanny/conf/database/DatabaseConfigLocal.sh > /dev/null
            sudo chmod a+x /var/lib/hootenanny/conf/database/DatabaseConfigLocal.sh
        else
        sudo sed -i s/DB_PASSWORD=.*/DB_PASSWORD=$RAND_PW/ /var/lib/hootenanny/conf/database/DatabaseConfig.sh
        fi
        sudo -u postgres createdb hoot --owner=hoot
        sudo -u postgres createdb wfsstoredb --owner=hoot
        sudo -u postgres psql -d hoot -c 'create extension hstore;'
        sudo -u postgres psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='wfsstoredb'"
        sudo -u postgres psql -d wfsstoredb -c 'create extension postgis;'
    fi

    # restore saved db config file settings if present
    if [ -f /var/lib/hootenanny/conf/database/DatabaseConfig.sh.rpmsave ]; then
        if [ -f /var/lib/hootenanny/conf/database/DatabaseConfigDefault.sh ]; then
            grep DB_PASSWORD /var/lib/hootenanny/conf/database/DatabaseConfig.sh.rpmsave | sudo tee /var/lib/hootenanny/conf/database/DatabaseConfigLocal.sh > /dev/null
            sudo chmod a+x /var/lib/hootenanny/conf/database/DatabaseConfigLocal.sh
        else
        sudo mv /var/lib/hootenanny/conf/database/DatabaseConfig.sh.rpmsave /var/lib/hootenanny/conf/database/DatabaseConfig.sh
    fi
    fi

    # configure Postgres settings
    PG_HB_CONF=/var/lib/pgsql/%{pg_version}/data/pg_hba.conf
    if ! sudo grep -i --quiet hoot $PG_HB_CONF; then
        sudo -u postgres sed -i '1ihost    all            hoot            127.0.0.1/32            md5' $PG_HB_CONF
        sudo -u postgres sed -i '1ihost    all            hoot            ::1/128                 md5' $PG_HB_CONF
    fi
    POSTGRES_CONF=/var/lib/pgsql/%{pg_version}/data/postgresql.conf
    if ! grep -i --quiet HOOT $POSTGRES_CONF; then
        sudo -u postgres sed -i s/^max_connections/\#max_connections/ $POSTGRES_CONF
        sudo -u postgres sed -i s/^shared_buffers/\#shared_buffers/ $POSTGRES_CONF
        sudo -u postgres bash -c "cat >> $POSTGRES_CONF" <<EOT
#--------------
# Hoot Settings
#--------------
max_connections = 1000
shared_buffers = 1024MB
max_files_per_process = 1000
work_mem = 16MB
maintenance_work_mem = 256MB
checkpoint_segments = 20
autovacuum = off
EOT
    fi
    # configure kernel parameters
    SYSCTL_CONF=/etc/sysctl.conf
    if ! grep --quiet 1173741824 $SYSCTL_CONF; then
        echo "Setting kernel.shmmax"
        sudo sysctl -w kernel.shmmax=1173741824
        sudo sh -c "echo 'kernel.shmmax=1173741824' >> $SYSCTL_CONF"
        #                 kernel.shmmax=68719476736
    fi
    if ! grep --quiet 2097152 $SYSCTL_CONF; then
        echo "Setting kernel.shmall"
        sudo sysctl -w kernel.shmall=2097152
        sudo sh -c "echo 'kernel.shmall=2097152' >> $SYSCTL_CONF"
        #                 kernel.shmall=4294967296
    fi
    sudo service postgresql-%{pg_version} restart

    # create the osm api test db
    /var/lib/hootenanny/scripts/database/SetupOsmApiDB.sh

    updateConfigFiles
    updateLiquibase

    # Configuring firewall
    if ! sudo iptables --list-rules | grep -i --quiet 'dport 80'; then
        sudo iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT
        sudo iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 8080 -j ACCEPT
        sudo iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 8000 -j ACCEPT
        sudo iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 8094 -j ACCEPT
        sudo iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 8096 -j ACCEPT
        sudo iptables -I PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 8080
        sudo iptables -I OUTPUT -t nat -s 0/0 -d 127/8 -p tcp --dport 80 -j REDIRECT --to-ports 8080
        sudo service iptables save
        sudo service iptables restart
    fi
elif [ "$1" = "2" ]; then
    # Perform whatever maintenance must occur after the upgrade

    # copy values from saved db config file, if present
    if [ -f /var/lib/hootenanny/conf/database/DatabaseConfig.sh.rpmsave ]; then
        if [ -f /var/lib/hootenanny/conf/database/DatabaseConfigDefault.sh ]; then
            grep DB_PASSWORD /var/lib/hootenanny/conf/database/DatabaseConfig.sh.rpmsave | sudo tee /var/lib/hootenanny/conf/database/DatabaseConfigLocal.sh > /dev/null
            sudo chmod a+x /var/lib/hootenanny/conf/database/DatabaseConfigLocal.sh
        else
            sudo mv /var/lib/hootenanny/conf/database/DatabaseConfig.sh.rpmsave /var/lib/hootenanny/conf/database/DatabaseConfig.sh
        fi
    fi

    source /etc/profile.d/hootenanny.sh
    source /var/lib/hootenanny/conf/database/DatabaseConfig.sh

    updateConfigFiles
    updateLiquibase
fi

%postun services-ui
if [ "$1" = "0" ]; then
    # Perform tasks to clean up after uninstallation

    # Stop tomcat
    sudo service tomcat8 stop
    # Ensure Postgres is started
    sudo service postgresql-%{pg_version} start
    while ! PG_VERSION=$(sudo -u postgres psql -c 'SHOW SERVER_VERSION;' | egrep -o '[0-9]{1,}\.[0-9]{1,}'); do
        echo "Waiting for postgres to start"
        sleep 1
    done

    # Remove .deegree directory
    TOMCAT_HOME=/usr/share/tomcat8
    if [ -d $TOMCAT_HOME/.deegree ]; then
        sudo rm -rf $TOMCAT_HOME/.deegree
    fi
    # Remove exploded hoot-services war remnants
    SERVICES_HOME=/var/lib/tomcat8/webapps/hoot-services
    if [ -d $SERVICES_HOME ]; then
        sudo rm -rf $SERVICES_HOME
    fi
    sudo service tomcat8 start

    # Configuring firewall
    if sudo iptables --list-rules | grep -i --quiet 'dport 80'; then
        sudo iptables -D INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT
        sudo iptables -D INPUT -p tcp -m state --state NEW -m tcp --dport 8080 -j ACCEPT
        sudo iptables -D INPUT -p tcp -m state --state NEW -m tcp --dport 8000 -j ACCEPT
        sudo iptables -D INPUT -p tcp -m state --state NEW -m tcp --dport 8094 -j ACCEPT
        sudo iptables -D INPUT -p tcp -m state --state NEW -m tcp --dport 8096 -j ACCEPT
        sudo iptables -D PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 8080
        sudo iptables -D OUTPUT -t nat -s 0/0 -d 127/8 -p tcp --dport 80 -j REDIRECT --to-ports 8080
        sudo service iptables save
        sudo service iptables restart
    fi
fi



%package    autostart
Summary:    Hootenanny Autostart
Requires:   %{name}-services-ui = %{version}-%{release}
Group:      Applications/Engineering

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
# set Postgres to autostart
sudo systemctl enable postgresql-%{pg_version}

# Turn off tomcat6 if installed
if /sbin/chkconfig | grep --quiet tomcat6 ; then
    sudo /sbin/chkconfig --del tomcat6
fi

# set Tomcat to autostart
sudo systemctl enable tomcat8

# set NodeJS node-mapnik-server to autostart
sudo /sbin/chkconfig --add node-mapnik-server
sudo /sbin/chkconfig node-mapnik-server on
# set NodeJS node-export-server to autostart
sudo /sbin/chkconfig --add node-export-server
sudo /sbin/chkconfig node-export-server on

%postun autostart
# set Postgres to NOT autostart
sudo /sbin/chkconfig --del postgresql-%{pg_version}
# set Tomcat to NOT autostart
sudo /sbin/chkconfig --del tomcat8
# set NodeJS node-mapnik-server to NOT autostart
sudo /sbin/chkconfig --del node-mapnik-server
# set NodeJS node-export-server to NOT autostart
sudo /sbin/chkconfig --del node-export-server

%package services-devel-deps
Summary:    Development dependencies for Hootenanny Services
Group:      Development/Libraries
Requires:   %{name}-core-devel-deps = %{version}-%{release}
Requires:   apache-maven
Requires:   nodejs
Requires:   npm
Requires:   postgresql%{pg_dotless}-server
Requires:   postgresql%{pg_dotless}-contrib
Requires:   hoot-postgis
Requires:   hoot-postgis-utils
Requires:   liquibase

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
if [ "$1" = "1" ]; then
    # Perform tasks to prepare for the initial installation

    # init and start Postgres
    sudo service postgresql-%{pg_version} initdb
    sudo service postgresql-%{pg_version} start
    while ! PG_VERSION=$(sudo -u postgres psql -c 'SHOW SERVER_VERSION;' | egrep -o '[0-9]{1,}\.[0-9]{1,}'); do
        echo "Waiting for postgres to start"
        sleep 1
    done

    sudo service tomcat8 start

    # create Hoot services db
    if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw hoot; then
        sudo -u postgres createuser --superuser hoot || true
        sudo -u postgres psql -c "alter user hoot with password 'hoottest';"
        sudo -u postgres createdb hoot --owner=hoot
        sudo -u postgres createdb wfsstoredb --owner=hoot
        sudo -u postgres psql -d hoot -c 'create extension hstore;'
        sudo -u postgres psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='wfsstoredb'"
        sudo -u postgres psql -d wfsstoredb -c 'create extension postgis;'
    fi

    # configure Postgres settings
    PG_HB_CONF=/var/lib/pgsql/%{pg_version}/data/pg_hba.conf
    if ! sudo grep -i --quiet hoot $PG_HB_CONF; then
        sudo -u postgres sed -i '1ihost    all            hoot            127.0.0.1/32            md5' $PG_HB_CONF
        sudo -u postgres sed -i '1ihost    all            hoot            ::1/128                 md5' $PG_HB_CONF
    fi
    POSTGRES_CONF=/var/lib/pgsql/%{pg_version}/data/postgresql.conf
    if ! grep -i --quiet HOOT $POSTGRES_CONF; then
        sudo -u postgres sed -i s/^max_connections/\#max_connections/ $POSTGRES_CONF
        sudo -u postgres sed -i s/^shared_buffers/\#shared_buffers/ $POSTGRES_CONF
        sudo -u postgres bash -c "cat >> $POSTGRES_CONF" <<EOT
#--------------
# Hoot Settings
#--------------
max_connections = 1000
shared_buffers = 1024MB
max_files_per_process = 1000
work_mem = 16MB
maintenance_work_mem = 256MB
checkpoint_segments = 20
autovacuum = off
EOT
    fi
    # configure kernel parameters
    SYSCTL_CONF=/etc/sysctl.conf
    if ! grep --quiet 1173741824 $SYSCTL_CONF; then
        echo "Setting kernel.shmmax"
        sudo sysctl -w kernel.shmmax=1173741824
        sudo sh -c "echo 'kernel.shmmax=1173741824' >> $SYSCTL_CONF"
        #                 kernel.shmmax=68719476736
    fi
    if ! grep --quiet 2097152 $SYSCTL_CONF; then
        echo "Setting kernel.shmall"
        sudo sysctl -w kernel.shmall=2097152
        sudo sh -c "echo 'kernel.shmall=2097152' >> $SYSCTL_CONF"
        #                 kernel.shmall=4294967296
    fi
    sudo service postgresql-%{pg_version} restart
fi

%postun services-devel-deps
if [ "$1" = "0" ]; then
    # Perform tasks to clean up after uninstallation

    # Ensure Postgres is started
    sudo service postgresql-%{pg_version} start
    while ! PG_VERSION=$(sudo -u postgres psql -c 'SHOW SERVER_VERSION;' | egrep -o '[0-9]{1,}\.[0-9]{1,}'); do
        echo "Waiting for postgres to start"
        sleep 1
    done
fi

%package core-devel-deps
Summary:    Development dependencies for Hootenanny Core
Group:      Development/Libraries
Requires:  %{name}-core-deps = %{version}-%{release}
Requires:  autoconf
Requires:  automake
Requires:  boost-devel
Requires:  cppunit-devel
Requires:  gcc-c++
Requires:  gdb
Requires:  geos-devel >= %{geos_min_version}
Requires:  git
Requires:  glpk-devel
Requires:  libicu-devel
Requires:  hoot-words >= 1.0.0
Requires:  libspatialite-devel
Requires:  log4cxx-devel
Requires:  nodejs-devel
Requires:  opencv-devel
Requires:  postgresql%{pg_dotless}-devel
Requires:  proj-devel
Requires:  protobuf-devel
Requires:  python-argparse
Requires:  python-devel
Requires:  qt-devel
Requires:  stxxl-devel
Requires:  v8-devel
Requires:  texlive

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
Summary:    Dependencies for Hootenanny Core
Group:      Development/Libraries
Requires:  asciidoc
Requires:  cppunit
Requires:  dblatex
Requires:  doxygen
Requires:  FileGDBAPI
Requires:  geos >= %{geos_min_version}
Requires:  gnuplot
Requires:  graphviz
Requires:  hoot-gdal-devel >= %{gdal_min_version}
Requires:  hoot-gdal-python >= %{gdal_min_version}
Requires:  hoot-words >= 1.0.0
# Needed by gnuplot for report generation
Requires:  liberation-fonts-common
Requires:  liberation-sans-fonts
Requires:  libxslt
Requires:  log4cxx
Requires:  nodejs
Requires:  opencv
Requires:  protobuf
Requires:  proj
Requires:  proj-devel
Requires:  qt
Requires:  qt-postgresql
Requires:  stxxl
Requires:  texlive
Requires:  unzip
Requires:  w3m
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

%changelog
* Wed Nov 08 2017 Matt Jackson <matthew.jacksondigitalglobe.com> - 0.2.36+
- Many Centos7 fixes

* Fri May 12 2017 Matt Jackson <matthew.jacksondigitalglobe.com> - 0.2.33+
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
