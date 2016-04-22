TARBALLS := $(wildcard SOURCES/hootenanny*.tar.gz)
DOCBALLS := $(wildcard SOURCES/hootenanny*-documentation.tar.gz)
HOOTBALL := $(filter-out $(DOCBALLS), $(TARBALLS))

FILEGDB_RPM=RPMS/x86_64/FileGDB_API-1.3-1.el6.x86_64.rpm
INSTALL_FILEGDB=yum list installed FileGDB_API || sudo yum -y install $(FILEGDB_RPM)
# Synchronizing the make build with rpmbuild parallel flags causes problems. This way we
# spawn at most nproc processes per sub-job and if the load is above nproc + 2 no more
# jobs will be spawned. This is a poor man parallelism, but should avoid killing the
# host.
RPMBUILD_OPTS=--define "_topdir `pwd`" --define "_smp_mflags -j`nproc` -l$$((`nproc` + 2))"

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
	RPMS/noarch/autoconf-2.69-3.el6.noarch.rpm \
	RPMS/noarch/dblatex-0.3-5.el6.noarch.rpm \
	RPMS/noarch/python-which-1.1.0-12.el6.noarch.rpm \
	$(FILEGDB_RPM) \
	RPMS/x86_64/gdal-1.10.1-3.el6.x86_64.rpm \
	RPMS/x86_64/gdal-esri-epsg-1.10.1-1.el6.x86_64.rpm \
	RPMS/x86_64/geos-3.4.2-2.el6.x86_64.rpm \
	RPMS/x86_64/gnuplot-4.6.1-1.el6.x86_64.rpm \
	RPMS/x86_64/log4cxx-0.10.0-14.el6.x86_64.rpm \
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

SPECS/hootenanny.spec: SPECS/hootenanny.spec.in  $(HOOTBALL)
	test $(words $(HOOTBALL)) == 0 && (echo "Did not find a hoot tarball in SOURCES. Do you need to download one? https://github.com/ngageoint/hootenanny/releases"; exit -1) || true
	test $(words $(HOOTBALL)) == 1 || (echo "Found more than 1 hoot tarball please remove the extra tarballs. $(HOOTBALL)"; exit -1)
	mv SPECS/hootenanny.spec /tmp/hootenanny-`date +%s`.spec || true
	echo "# Do not modify directly, please modify hootenanny.spec.in instead." > SPECS/hootenanny.spec
	cat SPECS/hootenanny.spec.in | sed -e "s/%%HOOT_VERSION%%/$(hootversion)/g" >> SPECS/hootenanny.spec

RPMS/x86_64/hootenanny-core-$(hootversion).el6.x86_64.rpm: SPECS/hootenanny.spec tmp/hoot-deps
	rm -rf BUILD/hootenanny-* BUILDROOT/hootenanny-* RPMS/x86_64/hootenanny-* SRPMS/hootenanny-*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

RPMS/noarch/autoconf-2.69-3.el6.noarch.rpm: SPECS/autoconf.spec
	rm -f RPMS/noarch/autoconf* RPMS/x86_64/autoconf*
	# autoconf fails intermittently with some odd test failures. See:
	# https://github.com/ngageoint/hootenanny-rpms/issues/62
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $< || MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

RPMS/noarch/dblatex-0.3-5.el6.noarch.rpm: SPECS/dblatex.spec tmp/python-which-install
	rm -f RPMS/noarch/dblatex* RPMS/x86_64/dblatex*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

$(FILEGDB_RPM): SPECS/FileGDB_API.spec
	rm -f RPMS/noarch/FileGDB_API* RPMS/x86_64/FileGDB_API*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

RPMS/x86_64/gdal-1.10.1-3.el6.x86_64.rpm: SPECS/gdal.spec $(FILEGDB_RPM)
	# The gdal-1* prevents deleting the gdal-esri-epsg RPM
	rm -f RPMS/noarch/gdal-1* RPMS/x86_64/gdal-1*
	$(INSTALL_FILEGDB)
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

RPMS/x86_64/geos-3.4.2-2.el6.x86_64.rpm: SPECS/geos.spec
	rm -f RPMS/noarch/geos* RPMS/x86_64/geos*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

RPMS/x86_64/gdal-esri-epsg-1.10.1-1.el6.x86_64.rpm: SPECS/gdal-esri-epsg.spec
	rm -f RPMS/noarch/gdal-esri-epsg* RPMS/x86_64/gdal-esri-epsg*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

RPMS/x86_64/gnuplot-4.6.1-1.el6.x86_64.rpm: SPECS/gnuplot.spec
	rm -f RPMS/noarch/gnuplot* RPMS/x86_64/gnuplot*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

RPMS/noarch/python-which-1.1.0-12.el6.noarch.rpm: SPECS/python-which.spec
	rm -f RPMS/noarch/python-which* RPMS/x86_64/python-which*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

RPMS/x86_64/log4cxx-0.10.0-14.el6.x86_64.rpm: SPECS/log4cxx.spec
	rm -f RPMS/noarch/log4cxx* RPMS/x86_64/log4cxx*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

RPMS/x86_64/stxxl-1.3.1-1.el6.x86_64.rpm: SPECS/stxxl.spec
	rm -f RPMS/noarch/stxxl* RPMS/x86_64/stxxl*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

RPMS/noarch/hootenanny-words-1.0.0-1.el6.noarch.rpm: SPECS/hootenanny-words.spec
	rm -f RPMS/noarch/hootenanny-words* RPMS/x86_64/hootenanny-words*
	MAKEFLAGS= rpmbuild $(RPMBUILD_OPTS) -ba $<

