TARBALLS := $(wildcard SOURCES/hootenanny*.tar.gz)
DOCBALLS := $(wildcard SOURCES/hootenanny*-documentation.tar.gz)
HOOTBALL := $(filter-out $(DOCBALLS), $(TARBALLS))

# Synchronizing the make build with rpmbuild parallel flags causes problems. This way we
# spawn at most nproc processes per sub-job and if the load is above nproc + 2 no more
# jobs will be spawned. This is a poor man parallelism, but should avoid killing the
# host.
# RPMBUILD_OPTS=--quiet --define "_topdir `pwd`" --define "_smp_mflags -j`nproc` -l$$((`nproc` + 2))"
RPMBUILD_OPTS=--define "_topdir `pwd`" --define "_smp_mflags -j`nproc` -l$$((`nproc` + 2))"

#Trying this
RPM_OPT_FLAGS=--std=c++11

hoottarball=$(lastword $(sort $(HOOTBALL)))

hootversion=$(patsubst SOURCES/hootenanny-%.tar.gz,%,$(hoottarball))

HOOT_RPM=RPMS/x86_64/hootenanny-core-$(hootversion).el7.x86_64.rpm

WORDS_RPM=RPMS/noarch/hootenanny-words-1.0.0-1.noarch.rpm
TOMCAT8_RPM=RPMS/noarch/tomcat8-8.5.23-1.el7.noarch.rpm
STXXL_RPM=RPMS/x86_64/stxxl-1.3.1-1.el7.x86_64.rpm

# GDAL depends on FileGDB and Postgis depends on GDAL
FILEGDB_RPM=RPMS/x86_64/FileGDBAPI-1.5.1-1.el7.centos.x86_64.rpm
POSTGIS_RPM=RPMS/x86_64/postgis-2.3.3-3.el7.centos.x86_64.rpm
GDAL_RPM=RPMS/x86_64/hoot-gdal-2.1.4-1.el7.x86_64.rpm

# all: not-hoot hoot
all: hoot

clean: clean-hoot
	rm -rf tmp BUILD/* BUILDROOT/* SRPMS/* RPMS/*

# Clean out all hoot specific RPMs and build files.
clean-hoot:
	rm -rf BUILD/hoot* BUILDROOT/hoot* SRPMS/hoot* RPMS/x86_64/hoot* SPECS/hootenanny.spec

not-hoot: tmp/not-hoot

# NOTE: POSTGIS_RPM installs GDAL RPM and GDAL_RPM installs FILEGDB_RPM
tmp/not-hoot: \
	$(WORDS_RPM) \
	$(TOMCAT8_RPM) \
	$(STXXL_RPM) \
	$(FILEGDB_RPM) \
	$(GDAL_RPM) \
	$(POSTGIS_RPM)
# touch was sometimes cropping down to second resolution
	echo > $@

hoot: $(HOOT_RPM)

tmp/hoot-deps: tmp/not-hoot
	# Adding bash to the end avoids an error if all the RPMs were already installed.
	sudo yum -y install --debuglevel=1 RPMS/x86_64/* RPMS/noarch/* bash
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

$(HOOT_RPM): SPECS/hootenanny.spec
	rm -rf BUILD/hootenanny-* BUILDROOT/hootenanny-* RPMS/x86_64/hootenanny-* SRPMS/hootenanny-*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

$(FILEGDB_RPM): SPECS/FileGDBAPI.spec
	rm -f RPMS/noarch/FileGDBAPI* RPMS/x86_64/FileGDBAPI*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

$(GDAL_RPM): SPECS/hoot-gdal.spec
	# The gdal-2* prevents deleting the gdal-esri-epsg RPM
	rm -f RPMS/noarch/hoot-gdal-2* RPMS/x86_64/hoot-gdal-2*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

$(POSTGIS_RPM): SPECS/postgis.spec
	rm -f RPMS/noarch/postgis* RPMS/x86_64/postgis*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

$(STXXL_RPM): SPECS/stxxl.spec
	rm -f RPMS/noarch/stxxl* RPMS/x86_64/stxxl*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

$(WORDS_RPM): SPECS/hootenanny-words.spec
	rm -f RPMS/noarch/hootenanny-words* RPMS/x86_64/hootenanny-words*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

$(TOMCAT8_RPM): SPECS/tomcat8.spec
	rm -f RPMS/noarch/tomcat* tomcat*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<
