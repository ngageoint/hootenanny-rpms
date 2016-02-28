TARBALLS := $(wildcard SOURCES/hootenanny*.tar.gz)
DOCBALLS := $(wildcard SOURCES/hootenanny*-documentation.tar.gz)
HOOTBALL := $(filter-out $(DOCBALLS), $(TARBALLS))

hoottarball=$(lastword $(sort $(HOOTBALL)))

hootversion=$(patsubst SOURCES/hootenanny-%.tar.gz,%,$(hoottarball))

all: not-hoot hoot

clean: clean-hoot
	rm -rf tmp BUILD/* BUILDROOT/* SRPMS/* RPMS/*

# Clean out all hoot specific RPMs and build files.
clean-hoot:
	rm -rf BUILD/hoot* BUILDROOT/hoot* SRPMS/hoot* RPMS/x86_64/hoot* SPECS/hootenanny.spec

not-hoot: \
	RPMS/noarch/autoconf-2.69-3.el6.noarch.rpm \
	RPMS/noarch/dblatex-0.3-5.el6.noarch.rpm \
	RPMS/noarch/python-which-1.1.0-12.el6.noarch.rpm \
	RPMS/x86_64/FileGDB_API-1.3-1.el6.x86_64.rpm \
	RPMS/x86_64/gdal-1.10.1-3.el6.x86_64.rpm \
	RPMS/x86_64/gdal-esri-epsg-1.10.1-1.el6.x86_64.rpm \
	RPMS/x86_64/geos-3.4.2-1.el6.x86_64.rpm \
	RPMS/x86_64/gnuplot-4.6.1-1.el6.x86_64.rpm \
	RPMS/x86_64/log4cxx-0.10.0-14.el6.x86_64.rpm \
	RPMS/x86_64/stxxl-1.3.1-1.el6.x86_64.rpm \

hoot: \
	RPMS/x86_64/hootenanny-core-$(hootversion).el6.x86_64.rpm \

hoot-deps: not-hoot
	# Silly way to force a replacement of the gdal/geos RPMs
	sudo yum -y remove gdal-devel gdal geos geos-devel
	sudo yum -y install RPMS/x86_64/* RPMS/noarch/* libspatialite-devel postgis2_92

tmp/FileGDB-install: RPMS/x86_64/FileGDB_API-1.3-1.el6.x86_64.rpm
	yum list installed FileGDB_API || sudo yum -y install $<
	mkdir -p tmp
	touch $@

tmp/log4cxx-install: RPMS/x86_64/log4cxx-0.10.0-14.el6.x86_64.rpm
	yum list installed log4cxx || sudo yum -y install RPMS/x86_64/log4cxx*
	mkdir -p tmp
	touch $@

tmp/python-which-install: RPMS/noarch/python-which-1.1.0-12.el6.noarch.rpm
	yum list installed python-which || sudo yum -y install $<
	mkdir -p tmp
	touch $@

# Just run the install part.
hoot-test-install: SPECS/hootenanny.spec
	rpmbuild --define "_topdir `pwd`" --short-circuit -bi SPECS/hootenanny.spec

SPECS/hootenanny.spec: SPECS/hootenanny.spec.in  $(HOOTBALL)
	test $(words $(HOOTBALL)) == 0 && (echo "Did not find a hoot tarball in SOURCES. Do you need to download one? https://github.com/ngageoint/hootenanny/releases"; exit -1) || true
	test $(words $(HOOTBALL)) == 1 || (echo "Found more than 1 hoot tarball please remove the extra tarballs. $(HOOTBALL)"; exit -1)
	mv SPECS/hootenanny.spec /tmp/hootenanny-`date +%s`.spec || true
	echo "# Do not modify directly, please modify hootenanny.spec.in instead." > SPECS/hootenanny.spec
	cat SPECS/hootenanny.spec.in | sed -e "s/%%HOOT_VERSION%%/$(hootversion)/g" >> SPECS/hootenanny.spec

RPMS/x86_64/hootenanny-core-$(hootversion).el6.x86_64.rpm: SPECS/hootenanny.spec hoot-deps
	rm -rf BUILD/hootenanny-* BUILDROOT/hootenanny-* RPMS/x86_64/hootenanny-* SRPMS/hootenanny-*
	rpmbuild --define "_topdir `pwd`" -ba $<

RPMS/noarch/autoconf-2.69-3.el6.noarch.rpm: SPECS/autoconf.spec
	rpmbuild --define "_topdir `pwd`" -ba $<

RPMS/noarch/dblatex-0.3-5.el6.noarch.rpm: SPECS/dblatex.spec tmp/python-which-install
	rpmbuild --define "_topdir `pwd`" -ba $<

RPMS/x86_64/FileGDB_API-1.3-1.el6.x86_64.rpm: SPECS/FileGDB_API.spec
	rpmbuild --define "_topdir `pwd`" -ba $<

RPMS/x86_64/gdal-1.10.1-3.el6.x86_64.rpm: SPECS/gdal.spec tmp/FileGDB-install
	rpmbuild --define "_topdir `pwd`" -ba $<

RPMS/x86_64/geos-3.4.2-1.el6.x86_64.rpm: SPECS/geos.spec
	rpmbuild --define "_topdir `pwd`" -ba $<

RPMS/x86_64/gdal-esri-epsg-1.10.1-1.el6.x86_64.rpm: SPECS/gdal-esri-epsg.spec tmp/FileGDB-install
	rpmbuild --define "_topdir `pwd`" -ba $<

RPMS/x86_64/gnuplot-4.6.1-1.el6.x86_64.rpm: SPECS/gnuplot.spec
	rpmbuild --define "_topdir `pwd`" -ba $<

RPMS/noarch/python-which-1.1.0-12.el6.noarch.rpm: SPECS/python-which.spec
	rpmbuild --define "_topdir `pwd`" -ba $<

RPMS/x86_64/log4cxx-0.10.0-14.el6.x86_64.rpm: SPECS/log4cxx.spec
	rpmbuild --define "_topdir `pwd`" -ba $<

RPMS/x86_64/stxxl-1.3.1-1.el6.x86_64.rpm: SPECS/stxxl.spec
	rpmbuild --define "_topdir `pwd`" -ba $<


