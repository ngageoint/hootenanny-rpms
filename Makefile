
# Default branch of hoot to build
# GIT_COMMIT?=origin/develop
GIT_COMMIT?=origin/1042_new

TARBALLS := $(wildcard src/SOURCES/hootenanny*.tar.gz)
DOCBALLS := $(wildcard src/SOURCES/hootenanny*-documentation.tar.gz)
HOOTBALL := $(filter-out $(DOCBALLS), $(TARBALLS))

all: copy-rpms

# a convenience target for building hoot RPMs and no others.
hoot-rpms:
	cd src; $(MAKE) hoot

force:

# Clean out all the RPMs
clean: clean-hoot
	cd src; $(MAKE) clean

# Clean out everything
clean-all: vagrant-clean clean

# Cleans out the RPM el7 stash, archive hoot, and all the hoot source/rpms
clean-hoot:
	rm -rf el7
	rm -rf tmp/hootenanny
	cd src; $(MAKE) clean-hoot

ValidHootTarball:
	test $(words $(HOOTBALL)) != 1 && (echo "Did not find exactly one hoot tarball in SOURCES. Too many? Do you need to download one? https://github.com/ngageoint/hootenanny/releases"; exit -1) || true

vagrant-build-up: vagrant-plugins
	vagrant up

copy-words1: vagrant-build-up
	# If we have words1.sqlite locally don't copy it down from github.
	([ -e /tmp/words1.sqlite ] && cat /tmp/words1.sqlite | vagrant ssh -c "cat > /tmp/words1.sqlite") || true

vagrant-plugins:
	# Install the bindfs plugin if it doesn't exist
	(vagrant plugin list | grep -q bindfs) || vagrant plugin install vagrant-bindfs

vagrant-build-deps: copy-words1
	vagrant ssh -c "cd hootenanny-rpms && make -j$$((`nproc` + 2)) deps"

vagrant-build: vagrant-build-rpms

vagrant-build-rpms: vagrant-build-archive
	vagrant up
	vagrant ssh -c "cd hootenanny-rpms && make -j$$((`nproc` + 2))"

vagrant-build-archive: vagrant-build-deps
	vagrant up
	vagrant ssh -c "export GIT_COMMIT=$(GIT_COMMIT) ; cd hootenanny-rpms && ./BuildArchive.sh"

vagrant-clean:
	vagrant halt
	vagrant destroy -f
	mkdir -p el7
	cd test && vagrant halt && vagrant destroy -f
	rmdir --ignore-fail-on-non-empty el7 || true
	rm -f src/tmp/*-install

vagrant-test:
	# Adding this in so we always have a clean test VM.
	cd test && vagrant halt && vagrant destroy -f
	cd test; vagrant up
	cd test; vagrant ssh -c "cd /var/lib/hootenanny && sudo HootTest --diff --slow"

# This spawns a small VM to update the main repo so we can copy it to S3
vagrant-repo:
	cd update-repo; vagrant up
	cd update-repo; vagrant destroy -f


# Get a copy of the Oracle 8 JDK
# As of 11/29/2016, the hootenanny-rpms project in Github supports files <= 100MB in size.
# Everything over this size gets rejected by Github.  In order to workaround this limitation,
# we download a copy of the 159Mb JDK and store it in the el7 directory. This ensures that it
# is installed and is copied to the S3 repo.
JDK_RPM=jdk-8u144-linux-x64.rpm
JDK_URL=http://download.oracle.com/otn-pub/java/jdk/8u144-b01/090f390dda5b47b9b721c7dfaa008135/jdk-8u144-linux-x64.rpm

el7-src/jdk-8u144-linux-x64.rpm:
	wget --quiet --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" $(JDK_URL) -P el7-src

# NOTE:
# We are installing  jasper-devel-1.900.1-29.el7 as a workaround due to https://bugs.centos.org/view.php?id=13276
deps: force el7-src/jdk-8u144-linux-x64.rpm
	sudo cp repos/*.repo /etc/yum.repos.d
	sudo cp repos/*-GPG-* /etc/pki/rpm-gpg/
	sudo yum clean metadata
	# Sometimes the yum update fails getting the metadata. Try several times and ignore
	# the first two if they error
	sudo yum update -y --exclude=puppet* || sleep 30
	sudo yum update -y --exclude=puppet* || sleep 30
	sudo yum update -y --exclude=puppet*
	sudo true || true
	sudo yum install -y yum-plugin-versionlock el7-src/*
	sudo yum versionlock nodejs*

	sudo yum install -y \
	ant \
	armadillo-devel \
	asciidoc \
	autoconf \
	automake \
	bash-completion \
	bc \
	boost-devel \
	ccache \
	cfitsio-devel \
	chrpath \
	cmake \
	cppunit-devel \
	dblatex \
	doxygen \
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
	hdf-devel \
	hdf-static \
	jasper-devel-1.900.1-29.el7 \
	json-c-devel \
	libicu-devel \
	libdap-devel \
	libgeotiff-devel \
	libgta-devel \
	libjpeg-turbo-devel \
	libpng-devel \
	librx-devel \
	libspatialite-devel \
	libtiff-devel \
	libtool \
	libwebp-devel \
	m4 \
	maven \
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
	perl-devel \
	perl-generators \
	perl-XML-LibXML \
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
	python34-numpy \
	python34-devel \
	qt \
	qt-devel \
	qt-postgresql \
	qtwebkit \
	qtwebkit-devel \
	rpm-build \
	sqlite-devel \
	swig \
	tex* \
	unixODBC-devel \
	unzip \
	v8-devel \
	w3m \
	words \
	xerces-c-devel \
	xorg-x11-server-Xvfb \
	zip \
	zlib-devel \
	SFCGAL-devel \
	byacc \
	flex \
	gtk2-devel \
	> Centos7_pkgInstall.txt

#	postgis23_95 \

	# Setting /usr/java/jdk1.8.0_144/bin/java's priority to something really atrocious to guarantee that it will be
	# the one used when alternatives' auto mode is used.
	sudo alternatives --install /usr/bin/java java /usr/java/jdk1.8.0_144/bin/java 999999
	sudo alternatives --install /usr/bin/javac javac /usr/java/jdk1.8.0_144/bin/javac 9999999
	sudo alternatives --set java /usr/java/jdk1.8.0_144/bin/java
	sudo alternatives --set javac /usr/java/jdk1.8.0_144/bin/javac
	sudo ln -s /usr/java/jdk1.8.0_144  /usr/lib/jvm/java

# Now remove OpenJDK so we use our version of JAVA
#sudo rpm -e --nodeps java-1.8.0-openjdk-headless java-1.8.0-openjdk-devel java-1.8.0-openjdk


# 	  CharLS-devel \
# 	  ImageMagick \
# 	 X ant \
# 	  apache-maven \
# 	  apr-devel \
# 	  apr-util-devel \
# 	 X armadillo-devel \
# 	  automake \
# 	 X bash-completion \
# 	  bison \
# 	  boost-devel \
# 	  cairo-devel \
# 	 X cfitsio-devel \
# 	 X chrpath \
# 	  cppunit-devel \
# 	  createrepo \
# 	  ctags \
# 	  curl-devel \
# 	  doxygen \
# 	  emacs \
# 	  emacs-el \
# 	  erlang \
# 	  expat-devel \
# 	  flex \
# 	  fontconfig-devel \
# 	 # freexl-devel \
# 	  g2clib-static \
# 	  gcc \
# 	  gcc-c++ \
# 	  gd-devel \
# 	 X giflib-devel \
# 	  git \
# 	  graphviz \
# 	 X hdf-devel \
# 	 X hdf-static \
# 	  hdf5-devel \
# 	  help2man \
# 	  info \
# 	 X json-c-devel \
# 	  libX11-devel \
# 	  libXfixes-devel \
# 	  libXrandr-devel \
# 	  libXrender-devel \
# 	  libXt-devel \
# 	 X libdap-devel \
# 	  libdrm-devel \
# 	 X libgeotiff-devel \
# 	 X libgta-devel \
# 	  libicu-devel \
# 	 X libjpeg-turbo-devel \
# 	  libotf \
# 	  libpng-devel \
# 	 X librx-devel \
# 	 X libspatialite-devel \
# 	 X libtiff-devel \
# 	  libtool \
# 	 X libwebp-devel \
# 	  libxslt \
# 	  libxslt \
# 	  lua-devel \
# 	  m17n-lib* \
# 	  m4 \
# 	 X mysql-devel \
# 	 X netcdf-devel \
# 	  nodejs \
# 	  npm \
# 	 X numpy \
# 	 X openjpeg2-devel \
# 	  pango-devel \
# 	 X pcre-devel \
# 	 X perl-generators \
# 	  php-devel \
# 	 X poppler-devel \
# 	  proj-devel \
# 	  pygtk2 \
# 	  python-argparse \
# 	  python-devel \
# 	  python-devel \
# 	  readline-devel \
# 	  rpm-build \
# 	  ruby \
# 	  ruby-devel \
# 	  source-highlight \
# 	 X sqlite-devel \
# 	  swig \
# 	  tetex-tex4ht \
# 	  tex* \
# 	  transfig \
# 	  unixODBC-devel \
# 	  w3m \
# 	  wget \
# 	  words \
# 	 X xerces-c-devel \
# 	  xz-devel \
# 	  zlib-devel \


el7: el7-src/* custom-rpms

copy-rpms: el7
	rm -rf el7
	mkdir -p el7
	cp -l el7-src/* el7/
	cp src/RPMS/noarch/* el7/
	cp src/RPMS/x86_64/* el7/
	createrepo el7

custom-rpms:
	cd src; $(MAKE)

