
all: copy-rpms

hoot: | hoot-rpms copy-rpms

hoot-rpms:
	cd src; $(MAKE) hoot

force:

clean: .PHONY
	rm -rf el6
	cd src; $(MAKE) clean

deps: force
	sudo true || true
	sudo cp repos/HootBuild.repo /etc/yum.repos.d
	sudo cp repos/RPM-GPG-KEY-EPEL-6 /etc/pki/rpm-gpg/
	sudo yum clean metadata
	sudo true || true
	sudo yum install -y \
	  ant \
	  armadillo-devel \
	  automake \
	  bison \
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
	  gd-devel 
	  giflib-devel \
	  git \
	  hdf-devel \
	  hdf5-devel \
	  hdf-static \
	  help2man \
	  info \
	  java-1.6.0-openjdk-devel \
	  java-devel \
	  libdap-devel \
	  libgta-devel \
	  libjpeg-turbo-devel \
	  libotf \
	  libpng-devel \
	  librx-devel \
	  libspatialite-devel \
	  libX11-devel \
	  libXt-devel \
	  libxslt \
	  lua-devel \
	  m17n-lib* \
	  m4 \
	  netcdf-devel \
	  pango-devel \
	  pcre-devel \
	  perl-macros \
	  proj-devel \
	  pygtk2 \
	  python-devel \
	  python-which \
	  readline-devel \
	  rpm-build \
	  ruby-devel \
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
	  texlive-base \
	  texlive-collection-latex \
	  texlive-collection-xetex \
	  texlive-collection-htmlxml \
	  texlive-epstopdf-bin \
	  texlive-xmltex-bin \
	  texlive-anysize \
	  texlive-appendix \
	  texlive-changebar \
	  texlive-jknapltx \
	  texlive-multirow \
	  texlive-overpic \
	  texlive-pdfpages \
	  texlive-subfigure \
	  texlive-stmaryrd \
	  texlive-latex \
	  chrpath \
	  expat-devel \
	  fontconfig-devel \
	  geos-devel \
	  libtool \
	  giflib-devel \
	  mysql-devel \
	  numpy \
	  poppler-devel \
	  postgresql-devel \
	  ruby \
	  swig \
	  unixODBC-devel \
	  gcc-c++ \
	  php-devel \
	  boost-devel \
	  libicu-devel \
	  cppunit-devel \
	  python-argparse \
	  el6-src/* \

el6: el6-src/* custom-rpms

copy-rpms: el6
	rm -rf el6
	mkdir -p el6
	cp -l el6-src/* el6/
	cp src/RPMS/noarch/* el6/
	cp src/RPMS/x86_64/* el6/
	createrepo el6

custom-rpms:
	cd src; $(MAKE)

