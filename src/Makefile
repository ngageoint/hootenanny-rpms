
hoottarball=$(lastword,$(sort,$(wildcard, SOURCES/hootenanny*.tar.gz)))

all: \
	RPMS/noarch/autoconf-2.69-3.el6.noarch.rpm \
	RPMS/noarch/dblatex-0.3.4-8.el6.noarch.rpm \
	RPMS/x86_64/FileGDB_API-1.3-1.el6.x86_64.rpm \
	RPMS/x86_64/gdal-1.10.1-3.el6.x86_64.rpm \
	RPMS/x86_64/gdal-esri-epsg-1.10.1-1.el6.x86_64.rpm \
	RPMS/x86_64/geos-3.4.2-1.el6.x86_64.rpm \

hoot: \
	RPMS/x86_64/hootenanny-core-0.2.20_204_gfc1455e_dirty-1.el6.x86_64.rpm \

RPMS/x86_64/hootenanny-core-0.2.20_204_gfc1455e_dirty-1.el6.x86_64.rpm: SPECS/hootenanny.spec
	rpmbuild -ba $<

RPMS/noarch/autoconf-2.69-3.el6.noarch.rpm: SPECS/autoconf.spec
	rpmbuild -ba $<

RPMS/noarch/dblatex-0.3.4-8.el6.noarch.rpm: SPECS/dblatex.spec
	rpmbuild -ba $<

RPMS/x86_64/FileGDB_API-1.3-1.el6.x86_64.rpm: SPECS/FileGDB_API.spec
	rpmbuild -ba $<

RPMS/x86_64/gdal-1.10.1-3.el6.x86_64.rpm: SPECS/gdal.spec
	rpmbuild -ba $<

RPMS/x86_64/geos-3.4.2-1.el6.x86_64.rpm: SPECS/geos.spec
	rpmbuild -ba $<

RPMS/x86_64/gdal-esri-epsg-1.10.1-1.el6.x86_64.rpm: SPECS/gdal-esri-epsg.spec
	rpmbuild -ba $<

