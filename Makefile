
# Default branch of hoot to build
GIT_COMMIT?=origin/develop
TARBALLS := $(wildcard src/SOURCES/hootenanny*.tar.gz)
DOCBALLS := $(wildcard src/SOURCES/hootenanny*-documentation.tar.gz)
HOOTBALL := $(filter-out $(DOCBALLS), $(TARBALLS))

# URL for downloading the Java8 JDK 
JDKURL=http://download.oracle.com/otn-pub/java/jdk/8u111-b14/jdk-8u111-linux-x64.rpm

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

# Cleans out the RPM el6 stash, archive hoot, and all the hoot source/rpms
clean-hoot:
	rm -rf el6
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


# NOTE: We grab a copy of the Oracle 8 JDK before installing the deps
vagrant-build-deps: copy-words1 el6-src/jdk-8u111-linux-x64.rpm
	vagrant ssh -c "cd hootenanny-rpms && make -j$$((`nproc` + 2)) deps"

vagrant-build: vagrant-build-rpms

vagrant-build-rpms: vagrant-build-archive
	vagrant up
	vagrant ssh -c "cd hootenanny-rpms && ./fix_postgres.sh"
	vagrant ssh -c "cd hootenanny-rpms && make -j$$((`nproc` + 2))"

vagrant-build-archive: vagrant-build-deps
	vagrant up
	vagrant ssh -c "export GIT_COMMIT=$(GIT_COMMIT) ; cd hootenanny-rpms && ./BuildArchive.sh"

vagrant-clean:
	vagrant halt
	vagrant destroy -f
	mkdir -p el6
	cd test && vagrant halt && vagrant destroy -f
	rmdir --ignore-fail-on-non-empty el6 || true
	rm -f src/tmp/*-install

vagrant-test:
	cd test; vagrant up
	cd test; vagrant ssh -c "cd /var/lib/hootenanny && sudo HootTest --diff \
		--exclude=.*ConflateAverageTest.sh \
		--exclude=.*RubberSheetConflateTest.sh \
		--exclude=.*ExactMatchInputsTest.sh \
		--slow"

# This spawns a small VM to update the main repo so we can copy it to S3
vagrant-repo:
	cd update-repo; vagrant up
	cd update-repo; vagrant destroy -f


# As of 11/29/2016, hootenanny-rpms project in Github supports files <= 100MB in size.  Everything over this size limit,
# will is currently rejected by Github.  In order to workaround this limitation, we will download a desired JDK RPM
# every time we build.
jdk_rpm = jdk-8u111-linux-x64.rpm
jdk_download_url = http://download.oracle.com/otn-pub/java/jdk/8u111-b14/jdk-8u111-linux-x64.rpm

install-java:
	(sudo yum list installed jdk1.8.0_111 > /dev/null 2>&1) || sudo wget --quiet --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" $(jdk_download_url) -P /tmp
	(sudo yum list installed jdk1.8.0_111 > /dev/null 2>&1) || sudo rpm -Uvh --force /tmp/$(jdk_rpm)

deps: force install-java
	sudo cp repos/HootBuild.repo /etc/yum.repos.d
	sudo cp repos/RPM-GPG-KEY-EPEL-6 /etc/pki/rpm-gpg/
	sudo yum clean metadata
	# Sometimes the yum update fails getting the metadata. Try several times and ignore
	# the first two if they error
	sudo yum update -y --exclude=puppet* || sleep 30
	sudo yum update -y --exclude=puppet* || sleep 30
	sudo yum update -y --exclude=puppet*
	sudo true || true
	sudo yum install -y \
	  ant \
	  apache-maven \
	  apr-devel \
	  apr-util-devel \
	  armadillo-devel \
	  automake \
	  bison \
	  bash-completion \
	  boost-devel \
	  cairo-devel \
	  cfitsio-devel \
	  CharLS-devel \
	  chrpath \
	  createrepo \
	  ctags \
	  curl-devel \
	  doxygen \
	  emacs \
	  emacs-el \
	  erlang \
	  flex \
	  freexl-devel \
	  g2clib-static \
	  gcc \
	  gd-devel \
	  giflib-devel \
	  git \
	  graphviz \
	  hdf-devel \
	  hdf5-devel \
	  hdf-static \
	  help2man \
	  info \
	  json-c-devel \
	  libdap-devel \
	  libgeotiff-devel \
	  libgta-devel \
	  libjpeg-turbo-devel \
	  libotf \
	  libpng-devel \
	  librx-devel \
	  libspatialite-devel \
	  libtiff-devel \
	  libwebp-devel \
	  libX11-devel \
	  libXt-devel \
	  libxslt \
	  lua-devel \
	  m17n-lib* \
	  m4 \
	  netcdf-devel \
	  nodejs \
	  npm \
	  openjpeg2-devel \
	  pango-devel \
	  pcre-devel \
	  perl-generators \
	  proj-devel \
	  pygtk2 \
	  python-devel \
	  readline-devel \
	  rpm-build \
	  ruby-devel \
	  source-highlight \
	  sqlite-devel \
	  tetex-tex4ht \
	  tex* \
	  transfig \
	  xerces-c-devel \
	  xz-devel \
	  zlib-devel \
	  wget \
	  w3m \
	  words \
	  rpm-build \
	  m4 \
	  emacs \
	  erlang \
	  python-devel \
	  libxslt \
	  ImageMagick \
	  expat-devel \
	  fontconfig-devel \
	  geos-devel \
	  libtool \
	  giflib-devel \
	  mysql-devel \
	  numpy \
	  poppler-devel \
	  ruby \
	  swig \
	  unixODBC-devel \
	  gcc-c++ \
	  php-devel \
	  libicu-devel \
	  cppunit-devel \
	  python-argparse \
	  libXrandr-devel \
	  libXrender-devel \
	  libdrm-devel \
	  el6-src/* \


el6: el6-src/* custom-rpms


# Get a copy of the Oracle 8 JDK
# As of 11/29/2016, the hootenanny-rpms project in Github supports files <= 100MB in size.  
# Everything over this size gets rejected by Github.  In order to workaround this limitation, 
# we download a copy of the 159Mb JDK and store it in the el6 directory. This ensures that it
# is installed and is copied to the S3 repo.
el6-src/jdk-8u111-linux-x64.rpm:
	wget --quiet --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" $(JDKURL) -P el6-src


copy-rpms: el6
	rm -rf el6
	mkdir -p el6
	cp -l el6-src/* el6/
	cp /tmp/$(jdk_rpm) el6/
	cp src/RPMS/noarch/* el6/
	cp src/RPMS/x86_64/* el6/
	createrepo el6

custom-rpms:
	cd src; $(MAKE)

