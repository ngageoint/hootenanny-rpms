
hoottarball=$(lastword $(sort $(wildcard SOURCES/hootenanny*.tar.gz)))

hootversion=$(patsubst SOURCES/hootenanny-%.tar.gz,%,$(hoottarball))

all: not-hoot hoot

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

hoot: \
	RPMS/x86_64/hootenanny-core-$(hootversion).el6.x86_64.rpm \

FileGDB-install: RPMS/x86_64/FileGDB_API-1.3-1.el6.x86_64.rpm
	yum list installed FileGDB_API || sudo yum install $<

python-which-install: RPMS/noarch/python-which-1.1.0-12.el6.noarch.rpm
	yum list installed python-which || sudo yum install $<

# Just run the install part.
hoot-test-install: SPECS/hootenanny.spec
	rpmbuild --short-circuit -bi SPECS/hootenanny.spec	

SPECS/hootenanny.spec: SPECS/hootenanny.spec.in $(wildcard SOURCES/hootenanny*.tar.gz)
	test "$(words $(wildcard SOURCES/hootenanny*.tar.gz))" == "0" && (echo "Did not find a hoot tarball in SOURCES. Do you need to download one? https://github.com/ngageoint/hootenanny/releases"; exit -1) || true
	test $(words $(wildcard SOURCES/hootenanny*.tar.gz)) == "1" || (echo "Found more than 1 hoot tarball please remove the extra tarballs. $(wildcard SOURCES/hootenanny*.tar.gz)"; exit -1)
	echo "# Do not modify directly, please modify hootenanny.spec.in instead." > SPECS/hootenanny.spec
	mv SPECS/hootenanny.spec /tmp/hootenanny-`date +%s`.spec || true
	cat SPECS/hootenanny.spec.in | sed -e "s/%%HOOT_VERSION%%/$(hootversion)/g" >> SPECS/hootenanny.spec

RPMS/x86_64/hootenanny-core-$(hootversion).el6.x86_64.rpm: SPECS/hootenanny.spec
	# Silly way to replace the gdal/geos RPMs
	sudo yum -y remove gdal-devel gdal geos geos-devel
	sudo yum -y install RPMS/x86_64/gdal-1.10.1-3.el6.x86_64.rpm RPMS/x86_64/gdal-devel-1.10.1-3.el6.x86_64.rpm RPMS/x86_64/geos-devel-3.4.2-1.el6.x86_64.rpm RPMS/x86_64/gdal-libs-1.10.1-3.el6.x86_64.rpm RPMS/x86_64/geos-3.4.2-1.el6.x86_64.rpm RPMS/x86_64/gdal-java-1.10.1-3.el6.x86_64.rpm
	rm -rf BUILD/hootenanny-* BUILDROOT/hootenanny-* RPMS/x86_64/hootenanny-* SRPMS/hootenanny-*
	rpmbuild -ba $<

RPMS/noarch/autoconf-2.69-3.el6.noarch.rpm: SPECS/autoconf.spec
	rpmbuild -ba $<

RPMS/noarch/dblatex-0.3-5.el6.noarch.rpm: SPECS/dblatex.spec python-which-install
	rpmbuild -ba $<

RPMS/x86_64/FileGDB_API-1.3-1.el6.x86_64.rpm: SPECS/FileGDB_API.spec
	rpmbuild -ba $<

RPMS/x86_64/gdal-1.10.1-3.el6.x86_64.rpm: SPECS/gdal.spec 
	rpmbuild -ba $<

RPMS/x86_64/geos-3.4.2-1.el6.x86_64.rpm: SPECS/geos.spec
	rpmbuild -ba $<

RPMS/x86_64/gdal-esri-epsg-1.10.1-1.el6.x86_64.rpm: SPECS/gdal-esri-epsg.spec FileGDB-install
	rpmbuild -ba $<

RPMS/x86_64/gnuplot-4.6.1-1.el6.x86_64.rpm: SPECS/gnuplot.spec
	rpmbuild -ba $<

RPMS/noarch/python-which-1.1.0-12.el6.noarch.rpm: SPECS/python-which.spec
	rpmbuild -ba $<

RPMS/x86_64/log4cxx-0.10.0-14.el6.x86_64.rpm: SPECS/log4cxx.spec
	rpmbuild -ba $<

