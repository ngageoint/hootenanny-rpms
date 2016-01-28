
all: el6

hoot: | hoot-rpms copy-rpms

hoot-rpms:
	cd src; $(MAKE) hoot

force:

clean: .PHONY
	rm -rf el6
	cd src; $(MAKE) clean

deps: force
	yum install -y ant armadillo-devel cfitsio-devel CharLS-devel curl-devel freexl-devel g2clib-static hdf-devel hdf5-devel hdf-static java-devel libgta-devel libspatialite-devel netcdf-devel libdap-devel librx-devel pcre-devel proj-devel ruby-devel sqlite-devel xerces-c-devel xz-devel java-1.6.0-openjdk-devel createrepo git doxygen wget w3m words automake gcc el6/FileGDB_API*.rpm rpm-build

el6: el6-src/* custom-rpms

copy-rpms: force
	rm -rf el6
	mkdir -p el6
	cp -l el6-src/* el6/
	cp src/RPMS/noarch/* el6/
	cp src/RPMS/x86_64/* el6/
	createrepo el6

custom-rpms:
	cd src; $(MAKE)

