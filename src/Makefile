TARBALLS := $(wildcard SOURCES/hootenanny*.tar.gz)
DOCBALLS := $(wildcard SOURCES/hootenanny*-documentation.tar.gz)
HOOTBALL := $(filter-out $(DOCBALLS), $(TARBALLS))

FILEGDB_RPM=RPMS/x86_64/FileGDB_API-1.5.1-1.el7.centos.x86_64.rpm
INSTALL_FILEGDB=yum list installed FileGDB_API || sudo yum -y install $(FILEGDB_RPM)
# Synchronizing the make build with rpmbuild parallel flags causes problems. This way we
# spawn at most nproc processes per sub-job and if the load is above nproc + 2 no more
# jobs will be spawned. This is a poor man parallelism, but should avoid killing the
# host.

POSTGISRPM=RPMS/x86_64/postgis-2.3.3-3.el7.centos.x86_64.rpm
INSTALL_POSTGIS=yum list installed postgis || sudo yum -y install $(POSTGISRPM)

# RPMBUILD_OPTS=--quiet --define "_topdir `pwd`" --define "_smp_mflags -j`nproc` -l$$((`nproc` + 2))"
RPMBUILD_OPTS=--define "_topdir `pwd`" --define "_smp_mflags -j`nproc` -l$$((`nproc` + 2))"

#Trying this
RPM_OPT_FLAGS=--std=c++11

hoottarball=$(lastword $(sort $(HOOTBALL)))

hootversion=$(patsubst SOURCES/hootenanny-%.tar.gz,%,$(hoottarball))

all: not-hoot hoot

clean: clean-hoot
	rm -rf tmp BUILD/* BUILDROOT/* SRPMS/* RPMS/*

# Clean out all hoot specific RPMs and build files.
clean-hoot:
	rm -rf BUILD/hoot* BUILDROOT/hoot* SRPMS/hoot* RPMS/x86_64/hoot* SPECS/hootenanny.spec

not-hoot: tmp/not-hoot

tmp/not-hoot: \
	RPMS/noarch/hootenanny-words-1.0.0-1.el6.noarch.rpm \
	RPMS/noarch/tomcat-8.5.20-1.el6.noarch.rpm \
	$(POSTGISRPM) \
	$(FILEGDB_RPM) \
	RPMS/x86_64/gdal-2.1.4-2.el6.x86_64.rpm \
	RPMS/x86_64/gdal-esri-epsg-2.1.4-2.el6.x86_64.rpm \
	RPMS/x86_64/stxxl-1.3.1-1.el6.x86_64.rpm
	# touch was sometimes cropping down to second resolution
	echo > $@

hoot: \
	RPMS/x86_64/hootenanny-core-$(hootversion).el6.x86_64.rpm \

tmp/hoot-deps: tmp/not-hoot
	# Adding bash to the end avoids an error if all the RPMs were already installed.
	sudo yum -y install RPMS/x86_64/* RPMS/noarch/* bash
	# touch was sometimes cropping down to second resolution
	echo > $@

tmp/log4cxx-install: RPMS/x86_64/log4cxx-0.10.0-14.el6.x86_64.rpm
	yum list installed log4cxx || sudo yum -y install RPMS/x86_64/log4cxx*
	mkdir -p tmp
	# touch was sometimes cropping down to second resolution
	echo > $@

tmp/python-which-install: RPMS/noarch/python-which-1.1.0-12.el6.noarch.rpm
	yum list installed python-which || sudo yum -y install $<
	mkdir -p tmp
	# touch was sometimes cropping down to second resolution
	echo > $@

# Just run the install part.
hoot-test-install: SPECS/hootenanny.spec
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) --short-circuit -bi SPECS/hootenanny.spec

# Just run the binary package part.
hoot-test-package: SPECS/hootenanny.spec
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) --short-circuit -bb SPECS/hootenanny.spec

SPECS/hootenanny.spec: SPECS/hootenanny.spec.in  $(HOOTBALL)
	test $(words $(HOOTBALL)) == 0 && (echo "Did not find a hoot tarball in SOURCES. Do you need to download one? https://github.com/ngageoint/hootenanny/releases"; exit -1) || true
	test $(words $(HOOTBALL)) == 1 || (echo "Found more than 1 hoot tarball please remove the extra tarballs. $(HOOTBALL)"; exit -1)
	mv SPECS/hootenanny.spec /tmp/hootenanny-`date +%s`.spec || true
	echo "# Do not modify directly, please modify hootenanny.spec.in instead." > SPECS/hootenanny.spec
	cat SPECS/hootenanny.spec.in | sed -e "s/%%HOOT_VERSION%%/$(hootversion)/g" >> SPECS/hootenanny.spec

RPMS/x86_64/hootenanny-core-$(hootversion).el6.x86_64.rpm: SPECS/hootenanny.spec tmp/hoot-deps
	rm -rf BUILD/hootenanny-* BUILDROOT/hootenanny-* RPMS/x86_64/hootenanny-* SRPMS/hootenanny-*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

$(FILEGDB_RPM): SPECS/FileGDB_API.spec
	rm -f RPMS/noarch/FileGDB_API* RPMS/x86_64/FileGDB_API*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

RPMS/x86_64/postgis-2.3.3-3.el7.centos.x86_64.rpm: SPECS/postgis.spec
	rm -f RPMS/noarch/postgis* RPMS/x86_64/postgis*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<


RPMS/x86_64/gdal-2.1.4-2.el6.x86_64.rpm: SPECS/gdal.spec $(FILEGDB_RPM)
	# The gdal-2* prevents deleting the gdal-esri-epsg RPM
	rm -f RPMS/noarch/gdal-2* RPMS/x86_64/gdal-2*
	$(INSTALL_FILEGDB)
	$(INSTALL_POSTGIS)
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

RPMS/x86_64/gdal-esri-epsg-2.1.4-2.el6.x86_64.rpm: SPECS/gdal-esri-epsg.spec
	rm -f RPMS/noarch/gdal-esri-epsg* RPMS/x86_64/gdal-esri-epsg*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

RPMS/noarch/python-which-1.1.0-12.el6.noarch.rpm: SPECS/python-which.spec
	rm -f RPMS/noarch/python-which* RPMS/x86_64/python-which*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

RPMS/x86_64/stxxl-1.3.1-1.el6.x86_64.rpm: SPECS/stxxl.spec
	rm -f RPMS/noarch/stxxl* RPMS/x86_64/stxxl*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

RPMS/noarch/hootenanny-words-1.0.0-1.el6.noarch.rpm: SPECS/hootenanny-words.spec
	rm -f RPMS/noarch/hootenanny-words* RPMS/x86_64/hootenanny-words*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

#As for 12/16/2016, there doesn't exist an official RPM for tomcat-8.5.20 release.  Build our own then.
RPMS/noarch/tomcat-8.5.20-1.el6.noarch.rpm: SPECS/tomcat8.spec
	rm -f RPMS/noarch/tomcat* tomcat*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<
