#!/usr/bin/env bash

set -e

# Link to make building easier
ln -s hootenanny-rpms/src/ rpmbuild

export LANG=en_US.UTF-8

# add EPEL repo for extra packages
echo "### Add epel repo ###" > CentOS_upgrade.txt
sudo yum -y install epel-release >> CentOS_upgrade.txt 2>&1

# add the Postgres repo
echo "### Add Postgres repo ###" > CentOS_upgrade.txt
sudo rpm -Uvh https://download.postgresql.org/pub/repos/yum/9.5/redhat/rhel-7-x86_64/pgdg-centos95-9.5-3.noarch.rpm  >> CentOS_upgrade.txt 2>&1

echo "Updating OS..."
echo "### Update ###" >> CentOS_upgrade.txt
sudo yum -q -y update >> CentOS_upgrade.txt 2>&1
echo "### Upgrade ###" >> CentOS_upgrade.txt
sudo yum -q -y upgrade >> CentOS_upgrade.txt 2>&1

# sudo cp repos/*.repo /etc/yum.repos.d
# sudo cp repos/*-GPG-* /etc/pki/rpm-gpg/
# sudo yum clean metadata

echo "### Installing the repo for an ancient version of NodeJS"
curl --silent --location https://rpm.nodesource.com/setup | sudo bash -

echo "### Installing an ancient version of NodeJS"
sudo yum install -y \
  nodejs-0.10.46 \
  nodejs-devel-0.10.46 \
  yum-plugin-versionlock

# Now try to lock NodeJS so that the next yum update doesn't remove it.
sudo yum versionlock nodejs*

# install useful and needed packages for working with hootenanny
echo "### Installing dependencies from repos..."
echo "  If this dies, check the Centos7_pkgInstall.txt file"
sudo yum -y install \
    hootenanny-rpms/el7-src/* \
    ant \
    armadillo-devel \
    asciidoc \
    autoconf \
    automake \
    bash-completion \
    bc \
    boost-devel \
    byacc \
    bzip2 \
    ccache \
    cfitsio-devel \
    chrpath \
    cmake \
    cppunit-devel \
    dblatex \
    doxygen \
    flex \
    freexl-devel \
    g2clib-static \
    gcc \
    gcc-c++ \
    gdb \
    geos \
    geos-devel \
    giflib-devel \
    git \
    git-core \
    glpk \
    glpk-devel \
    gnuplot \
    gtk2-devel \
    hdf-devel \
    hdf-static \
    jasper-devel-1.900.1-29.el7 \
    java-1.8.0-openjdk \
    java-1.8.0-openjdk-devel \
    json-c-devel \
    libdap-devel \
    libgeotiff-devel \
    libgta-devel \
    libicu-devel \
    libjpeg-turbo-devel \
    libpng-devel \
    librx-devel \
    libspatialite-devel \
    libtiff-devel \
    libtool \
    libwebp-devel \
    m4 \
    maven \
    mlocate \
    mysql-devel \
    netcdf-devel \
    numpy \
    ogdi-devel \
    opencv \
    opencv-core \
    opencv-devel \
    opencv-python \
    openjpeg2-devel \
    pcre-devel \
    perl-XML-LibXML \
    perl-XML-LibXML \
    perl-devel \
    perl-generators \
    poppler-devel \
    postgresql95 \
    postgresql95-contrib \
    postgresql95-devel \
    postgresql95-server \
    proj \
    proj-devel \
    protobuf \
    protobuf-compiler \
    protobuf-devel \
    python  \
    python-devel \
    python-matplotlib \
    python-pip  \
    python-setuptools \
    python34-devel \
    python34-numpy \
    qt \
    qt-devel \
    qt-postgresql \
    qtwebkit \
    qtwebkit-devel \
    redhat-lsb-core \
    rpm-build \
    SFCGAL-devel \
    sqlite-devel \
    swig \
    tex-fonts-hebrew \
    texlive \
    texlive-collection-fontsrecommended \
    texlive-collection-langcyrillic \
    unixODBC-devel \
    unzip \
    v8-devel \
    vim \
    w3m \
    wget \
    words \
    xerces-c-devel \
    xorg-x11-server-Xvfb \
    zlib-devel \
    zip  > Centos7_pkgInstall.txt

# NOTE: postgis gets built later
#   postgis23_95 \


# Get ready for build RPM's
echo "%__make /usr/bin/make -sj$(nproc)" >> ~/.rpmmacros

# Now setup stuff for building hootenanny
# First, Postgres
# Need to figure out a way to do this automagically
#PG_VERSION=9.5
PG_VERSION=$(psql --version | egrep -o '[0-9]{1,}\.[0-9]{1,}')

# Defensive.
cd /tmp

sudo PGSETUP_INITDB_OPTIONS="-E 'UTF-8' --lc-collate='en_US.UTF-8' --lc-ctype='en_US.UTF-8'" /usr/pgsql-$PG_VERSION/bin/postgresql95-setup initdb
sudo systemctl start postgresql-$PG_VERSION
sudo systemctl enable postgresql-$PG_VERSION

if ! grep --quiet "psql-" ~/.bash_profile; then
    echo "Adding PostGres path vars to profile..."
    echo "export PATH=\$PATH:/usr/pgsql-$PG_VERSION/bin" >> ~/.bash_profile
    source ~/.bash_profile
fi

if [ ! -f /etc/ld.so.conf.d/postgres$PG_VERSION.conf ]; then
    sudo sh -c "echo '/usr/pgsql-$PG_VERSION/lib' > /etc/ld.so.conf.d/postgres$PG_VERSION.conf"
    sudo ldconfig
fi

