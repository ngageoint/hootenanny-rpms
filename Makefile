
all: el6

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
	sudo yum install -y ant armadillo-devel cfitsio-devel CharLS-devel curl-devel freexl-devel g2clib-static hdf-devel hdf5-devel hdf-static java-devel libgta-devel libspatialite-devel netcdf-devel libdap-devel librx-devel pcre-devel proj-devel ruby-devel sqlite-devel xerces-c-devel xz-devel java-1.6.0-openjdk-devel createrepo git doxygen wget w3m words automake gcc rpm-build m4 emacs perl-macros erlang el6-src/perl-macros-1.0-20.1.i686.rpm el6-src/m4-* python-devel python-which libxslt ImageMagick texlive-base texlive-collection-latex texlive-collection-xetex texlive-collection-htmlxml transfig texlive-epstopdf-bin texlive-xmltex-bin texlive-anysize texlive-appendix texlive-changebar texlive-jknapltx texlive-multirow texlive-overpic texlive-pdfpages texlive-subfigure texlive-stmaryrd texlive-latex chrpath expat-devel fontconfig-devel geos-devel libtool giflib-devel mysql-devel numpy poppler-devel postgresql-devel ruby swig unixODBC-devel gcc-c++ php-devel boost-devel libicu-devel el6-src/* cppunit-devel python-argparse


el6: el6-src/* custom-rpms
	rm -rf el6
	mkdir -p el6
	cp -l el6-src/* el6/
	cp src/RPMS/noarch/* el6/
	cp src/RPMS/x86_64/* el6/
	createrepo el6

custom-rpms:
	cd src; $(MAKE)

