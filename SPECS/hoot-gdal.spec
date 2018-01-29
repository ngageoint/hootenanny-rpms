#TODO: g2clib and grib (said to be modified)
#TODO: Python 3 modules should be possible since 1.7
#TODO: Create script to make clean tarball
#TODO: msg needs to have PublicDecompWT.zip from EUMETSAT, which is not free;
#      Building without msg therefore
#TODO: e00compr bundled?
#TODO: There are tests for bindings -- at least for Perl
#TODO: Java has a directory with test data and a build target called test
#      It uses %%{JAVA_RUN}; make test seems to work in the build directory
#TODO: e00compr source is the same in the package and bundled in GDAL
#TODO: Consider doxy patch from Suse, setting EXTRACT_LOCAL_CLASSES  = NO

# Soname should be bumped on API/ABI break
# http://trac.osgeo.org/gdal/ticket/4543

# Conditionals and structures for EL 5 are there
# to make life easier for downstream ELGIS.
# Sadly noarch doesn't work in EL 5, see
# http://fedoraproject.org/wiki/EPEL/GuidelinesAndPolicies

# He also suggest to use --with-static-proj4 to actually link to proj, instead of dlopen()ing it.

# Major digit of the proj so version
%global proj_somaj 0

# Tests can be of a different version
%global testversion 2.1.4
%global run_tests 0

# Set to 1 to enable spatialite support; disabled by default.
%global with_spatialite 0

# No ppc64 build for spatialite in EL6
# https://bugzilla.redhat.com/show_bug.cgi?id=663938
%if 0%{?rhel} == 6
%ifnarch ppc64
%global with_spatialite 0
%endif
%endif


Name:		hoot-gdal
Version:	2.1.4
Release:	2%{?dist}
Summary:	GIS file format library
Group:		System Environment/Libraries
License:	MIT
URL:		http://www.gdal.org

Source0:	http://download.osgeo.org/gdal/%{version}/gdal-%{version}.tar.xz
Source1:	http://download.osgeo.org/gdal/%{testversion}/gdalautotest-%{testversion}.tar.gz
Source2:	gdal.pom

# Patch to use system g2clib
Patch1:		gdal-g2clib.patch
# Patch for Fedora JNI library location
Patch2:		gdal-jni.patch
# Fix bash-completion install dir
Patch3:		gdal-completion.patch
# Fix uchar type
Patch4:		gdal-uchar.patch

# Fedora uses Alternatives for Java
Patch8:		gdal-1.9.0-java.patch
Patch9:		gdal-2.1.0-zlib.patch

BuildRoot:	%{_tmppath}/gdal-%{version}-%{release}-root-%(%{__id_u} -n)

# Adding FileGDB API for Hootenanny
BuildRequires:  FileGDBAPI

BuildRequires:  ant
# No armadillo in EL5
BuildRequires:	armadillo-devel
BuildRequires:	bash-completion
BuildRequires:	cfitsio-devel
# No CharLS in EL5
#BuildRequires: CharLS-devel
BuildRequires:	chrpath
BuildRequires:	curl-devel
BuildRequires:	doxygen
BuildRequires:	expat-devel
BuildRequires:	fontconfig-devel
# No freexl in EL5
BuildRequires:	freexl-devel
BuildRequires:	g2clib-static
BuildRequires:	geos-devel
BuildRequires:	ghostscript
BuildRequires:	hdf-devel
BuildRequires:	hdf-static
BuildRequires:	hdf5-devel
BuildRequires:	java-devel >= 1:1.6.0
BuildRequires:	jasper-devel
BuildRequires:	jpackage-utils
BuildRequires:	json-c-devel
BuildRequires:	libgeotiff-devel
# No libgta in EL5
BuildRequires:	libgta-devel

BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
# No libkml in EL
BuildRequires:	libkml-devel

%if %{with_spatialite}
%global spatialite "--with-spatialite"
BuildRequires:	libspatialite-devel
%else
%global spatialite "--without-spatialite"
%endif

BuildRequires:	libtiff-devel
# No libwebp in EL 5 and 6
BuildRequires:	libwebp-devel
BuildRequires:	libtool
BuildRequires:	giflib-devel
BuildRequires:	netcdf-devel
BuildRequires:	libdap-devel
BuildRequires:	librx-devel
BuildRequires:	mysql-devel
BuildRequires:	numpy
BuildRequires:	python34-numpy
BuildRequires:	pcre-devel
BuildRequires:	ogdi-devel
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	openjpeg2-devel
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	%{_bindir}/pkg-config
BuildRequires:	poppler-devel
BuildRequires:	postgresql%{pg_dotless}-devel
BuildRequires:	proj-devel
BuildRequires:	python2-devel
BuildRequires:	python34-devel
BuildRequires:	sqlite-devel
BuildRequires:	swig
BuildRequires:	texlive-latex
%if 0%{?fedora} >= 20
BuildRequires:	texlive-collection-fontsrecommended
BuildRequires:	texlive-collection-langcyrillic
BuildRequires:	texlive-collection-langportuguese
BuildRequires:	texlive-collection-latex
BuildRequires:	texlive-epstopdf
BuildRequires:	tex(multirow.sty)
BuildRequires:	tex(sectsty.sty)
BuildRequires:	tex(tocloft.sty)
BuildRequires:	tex(xtab.sty)
%endif
BuildRequires:	unixODBC-devel
BuildRequires:	xerces-c-devel
BuildRequires:	xz-devel
BuildRequires:	zlib-devel

# Note that we conflict with EPEL's GDAL.
Conflicts:	gdal

# Run time dependency for gpsbabel driver
Requires:	gpsbabel

# proj DL-opened in ogrct.cpp, see also fix in %%prep
# %if 0%{?__isa_bits} == 64
# Requires:	libproj.so.%{proj_somaj}()(64bit)
# %else
# Requires:	libproj.so.%{proj_somaj}
# %endif

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

# Enable/disable generating refmans
%global build_refman 1

# We have multilib triage
%if "%{_lib}" == "lib"
  %global cpuarch 32
%else
  %global cpuarch 64
%endif

%if ! (0%{?fedora} || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

#TODO: Description on the lib?
%description
Geospatial Data Abstraction Library (GDAL/OGR) is a cross platform
C++ translator library for raster and vector geospatial data formats.
As a library, it presents a single abstract data model to the calling
application for all supported formats. It also comes with a variety of
useful commandline utilities for data translation and processing.

It provides the primary data access engine for many applications.
GDAL/OGR is the most widely used geospatial data access library.


%package devel
Summary:	Development files for the GDAL file format library
Group:	Development/Libraries
Conflicts:	gdal-devel

# Old rpm didn't figure out
%if 0%{?rhel} < 6
Requires: pkgconfig
%endif

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs
Obsoletes:	%{name}-static < 1.9.0-1

%description devel
This package contains development files for GDAL.


%package libs
Summary:	GDAL file format library
Group:		System Environment/Libraries
Conflicts:	gdal-libs

%description libs
This package contains the GDAL file format library.


%package java
Summary:	Java modules for the GDAL file format library
Group:		Development/Libraries
Conflicts:	gdal-java
Requires:	jpackage-utils
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description java
The GDAL Java modules provide support to handle multiple GIS file formats.


%package javadoc
Summary:	Javadocs for %{name}
Group:		Documentation
Conflicts:	gdal-javadoc
Requires:	jpackage-utils
BuildArch:	noarch

%description javadoc
This package contains the API documentation for %{name}.


%package perl
Summary:	Perl modules for the GDAL file format library
Group:		Development/Libraries
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Conflicts:	gdal-perl

%description perl
The GDAL Perl modules provide support to handle multiple GIS file formats.


%package python
Summary:	Python modules for the GDAL file format library
Group:		Development/Libraries
Requires:	numpy
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Conflicts:	gdal-python

%description python
The GDAL Python modules provide support to handle multiple GIS file formats.
The package also includes a couple of useful utilities in Python.


%package python3
Summary:	Python modules for the GDAL file format library
Group:		Development/Libraries
Requires:	python34-numpy
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Conflicts:	gdal-python3

%description python3
The GDAL Python 3 modules provide support to handle multiple GIS file formats.


%package doc
Summary:	Documentation for GDAL
Group:		Documentation
BuildArch:	noarch
Conflicts:	gdal-doc

%description doc
This package contains HTML and PDF documentation for GDAL.

# We don't want to provide private Python extension libs
%global __provides_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/.*\.so$

%prep
#%setup -q -n %{name}-%{version}-fedora -a 1
%setup -q -n gdal-%{version} -a 1

# Delete bundled libraries
rm -rf frmts/zlib
rm -rf frmts/png/libpng
rm -rf frmts/gif/giflib
rm -rf frmts/jpeg/libjpeg \
    frmts/jpeg/libjpeg12
rm -rf frmts/gtiff/libgeotiff \
    frmts/gtiff/libtiff
rm -r frmts/grib/degrib18/g2clib-1.0.4

%patch1 -p1 -b .g2clib~
%patch2 -p1 -b .jni~
%patch3 -p1 -b .completion~
%patch4 -p1 -b .uchar~
%patch8 -p1 -b .java~
%patch9 -p1 -b .zlib~

# Sanitize linebreaks and encoding
#TODO: Don't touch data directory!
# /frmts/grib/degrib18/degrib/metaname.cpp
# and geoconcept.c are potentially dangerous to change
set +x
for f in `find . -type f` ; do
  if file $f | grep -q ISO-8859 ; then
    set -x
    iconv -f ISO-8859-1 -t UTF-8 $f > ${f}.tmp && \
      mv -f ${f}.tmp $f
    set +x
  fi
  if file $f | grep -q CRLF ; then
    set -x
    sed -i -e 's|\r||g' $f
    set +x
  fi
done
set -x

# Solved for 2.0
for f in ogr/ogrsf_frmts/gpsbabel ogr/ogrsf_frmts/pgdump port apps; do
pushd $f
  chmod 644 *.cpp *.h
popd
done

# Replace hard-coded library- and include paths
sed -i 's|@LIBTOOL@|%{_bindir}/libtool|g' GDALmake.opt.in
sed -i 's|-L\$with_cfitsio -L\$with_cfitsio/lib -lcfitsio|-lcfitsio|g' configure
sed -i 's|-I\$with_cfitsio -I\$with_cfitsio/include|-I\$with_cfitsio/include/cfitsio|g' configure
sed -i 's|-L\$with_netcdf -L\$with_netcdf/lib -lnetcdf|-lnetcdf|g' configure
sed -i 's|-L\$DODS_LIB -ldap++|-ldap++|g' configure
sed -i 's|-L\$with_ogdi -L\$with_ogdi/lib -logdi|-logdi|g' configure
sed -i 's|-L\$with_jpeg -L\$with_jpeg/lib -ljpeg|-ljpeg|g' configure
sed -i 's|-L\$with_libtiff\/lib -ltiff|-ltiff|g' configure
sed -i 's|-lgeotiff -L$with_geotiff $LIBS|-lgeotiff $LIBS|g' configure
sed -i 's|-L\$with_geotiff\/lib -lgeotiff $LIBS|-lgeotiff $LIBS|g' configure

# libproj is dlopened; upstream sources point to .so, which is usually not present
# http://trac.osgeo.org/gdal/ticket/3602
sed -i 's|libproj.so|libproj.so.%{proj_somaj}|g' ogr/ogrct.cpp

# Fix Python installation path
sed -i 's|setup.py install|setup.py install --root=%{buildroot}|' swig/python/GNUmakefile

# Fix Python samples to depend on correct interpreter
mkdir -p swig/python3/samples
pushd swig/python/samples
for f in `find . -name '*.py'`; do
  sed 's|^#!.\+python$|#!/usr/bin/python3|' $f > ../../python3/samples/$f
  chmod --reference=$f ../../python3/samples/$f
  sed -i 's|^#!.\+python$|#!/usr/bin/python2|' $f
done
popd

# Adjust check for LibDAP version
# http://trac.osgeo.org/gdal/ticket/4545
%if %cpuarch == 64
  sed -i 's|with_dods_root/lib|with_dods_root/lib64|' configure
%endif

# Fix mandir
sed -i "s|^mandir=.*|mandir='\${prefix}/share/man'|" configure

# Add our custom cflags when trying to find geos
# https://bugzilla.redhat.com/show_bug.cgi?id=1284714
sed -i 's|CFLAGS=\"${GEOS_CFLAGS}\"|CFLAGS=\"${CFLAGS} ${GEOS_CFLAGS}\"|g' configure

%build
#TODO: Couldn't I have modified that in the prep section?
%ifarch sparcv9 sparc64 s390 s390x
export CFLAGS="$RPM_OPT_FLAGS -fPIC $(pkg-config FileGDBAPI --cflags)"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpic $(pkg-config FileGDBAPI --cflags)"
%endif
export CXXFLAGS="$CFLAGS -I%{_includedir}/libgeotiff"
export CPPFLAGS="$CPPFLAGS $(pkg-config FileGDBAPI --cflags) -I%{_includedir}/libgeotiff"

# For future reference:
# epsilon: Stalled review -- https://bugzilla.redhat.com/show_bug.cgi?id=660024
# Building without pgeo driver, because it drags in Java

%configure \
        LIBS=-lgrib2c \
        --with-autoload=%{_libdir}/gdalplugins \
        --datadir=%{_datadir}/gdal/ \
        --includedir=%{_includedir}/gdal/ \
        --prefix=%{_prefix}	\
        --without-bsb		\
        --with-armadillo	\
        --with-curl		\
        --with-cfitsio=%{_prefix}	\
        --with-dods-root=%{_prefix}	\
        --with-expat		\
        --with-fgdb		\
        --with-freexl		\
        --with-geos		\
        --with-geotiff=external	\
        --with-gif		\
        --with-gta		\
        --with-hdf4		\
        --with-hdf5		\
        --with-jasper		\
        --with-java		\
        --with-jpeg		\
        --with-libjson-c	\
        --without-jpeg12	\
        --with-liblzma		\
        --with-libtiff=external	\
        --with-libz		\
        --without-mdb		\
        --with-mysql		\
        --with-netcdf		\
        --with-odbc		\
        --with-ogdi		\
        --without-msg		\
        --with-openjpeg		\
        --with-pcraster		\
        --with-pg=%{pginstdir}/bin/pg_config		\
        --with-png		\
        --with-poppler		\
        %{spatialite}		\
        --with-sqlite3		\
        --with-threads		\
        --with-webp		\
        --with-xerces		\
        --enable-shared		\
        --with-perl		\
        --with-python		\
        --with-libkml

# {?_smp_mflags} doesn't work; Or it does -- who knows!
#make %{?_smp_mflags}
make -s
make -s man
make -s docs

# Make Perl modules
pushd swig/perl
  perl Makefile.PL;  make -s;
  echo > Makefile.PL;
popd

# Build some utilities, as requested in BZ #1271906
pushd ogr/ogrsf_frmts/s57/
  make -s all
popd

pushd frmts/iso8211/
  make -s all
popd

# Install the Perl modules in the right place
sed -i 's|INSTALLDIRS = site|INSTALLDIRS = vendor|' swig/perl/Makefile_*

# Don't append installation info to pod
#TODO: What about the pod?
sed -i 's|>> $(DESTINSTALLARCHLIB)\/perllocal.pod|> \/dev\/null|g' swig/perl/Makefile_*

# Make Java module and documentation
pushd swig/java
  make -s
  ./make_doc.sh
popd

# Make Python 3 module
pushd swig/python
  %{__python3} setup.py build
popd

# --------- Documentation ----------

# No useful documentation in swig
%global docdirs apps doc doc/br doc/ru ogr ogr/ogrsf_frmts frmts/gxf frmts/iso8211 frmts/pcidsk frmts/sdts frmts/vrt ogr/ogrsf_frmts/dgn/
for docdir in %{docdirs}; do
  # CreateHTML and PDF documentation, if specified
  pushd $docdir
    if [ ! -f Doxyfile ]; then
      doxygen -g
    else
      doxygen -u
    fi
    sed -i -e 's|^GENERATE_LATEX|GENERATE_LATEX = YES\n#GENERATE_LATEX |' Doxyfile
    sed -i -e 's|^GENERATE_HTML|GENERATE_HTML = YES\n#GENERATE_HTML |' Doxyfile
    sed -i -e 's|^USE_PDFLATEX|USE_PDFLATEX = YES\n#USE_PDFLATEX |' Doxyfile

    if [ $docdir == "doc/ru" ]; then
      sed -i -e 's|^OUTPUT_LANGUAGE|OUTPUT_LANGUAGE = Russian\n#OUTPUT_LANGUAGE |' Doxyfile
    fi
    rm -rf latex html
    doxygen

    %if %{build_refman}
      pushd latex
        sed -i -e '/rfoot\[/d' -e '/lfoot\[/d' doxygen.sty
        sed -i -e '/small/d' -e '/large/d' refman.tex
        sed -i -e 's|pdflatex|pdflatex -interaction nonstopmode |g' Makefile
        make -s refman.pdf || true
      popd
    %endif
  popd
done


%install
rm -rf %{buildroot}

# Install Python 3 module
# Must be done first so executables are Python 2.
pushd swig/python
  %{__python3} setup.py install --skip-build --root %{buildroot}
popd

make -s	DESTDIR=%{buildroot}	\
        install	\
        install-man

install -pm 755 ogr/ogrsf_frmts/s57/s57dump %{buildroot}%{_bindir}
install -pm 755 frmts/iso8211/8211createfromxml %{buildroot}%{_bindir}
install -pm 755 frmts/iso8211/8211dump %{buildroot}%{_bindir}
install -pm 755 frmts/iso8211/8211view %{buildroot}%{_bindir}

# Directory for auto-loading plugins
mkdir -p %{buildroot}%{_libdir}/gdalplugins

#TODO: Don't do that?
find %{buildroot}%{perl_vendorarch} -name "*.dox" -exec rm -rf '{}' \;
rm -f %{buildroot}%{perl_archlib}/perllocal.pod

# Correct permissions
#TODO and potential ticket: Why are the permissions not correct?
find %{buildroot}%{perl_vendorarch} -name "*.so" -exec chmod 755 '{}' \;
find %{buildroot}%{perl_vendorarch} -name "*.pm" -exec chmod 644 '{}' \;

#TODO: JAR files that require JNI shared objects MUST be installed in %%{_libdir}/%%{name}. The JNI shared objects themselves must also be installed in %%{_libdir}/%%{name}.
#Java programs that wish to make calls into native libraries do so via the Java Native Interface (JNI). A Java package uses JNI if it contains a .so
#If the JNI-using code calls System.loadLibrary you'll have to patch it to use System.load, passing it the full path to the dynamic shared object. If the package installs a wrapper script you'll need to manually add %%{_libdir}/%%{name}/<jar filename> to CLASSPATH. If you are depending on a JNI-using JAR file, you'll need to add it manually -- build-classpath will not find it.
touch -r NEWS swig/java/gdal.jar
mkdir -p %{buildroot}%{_javadir}
cp -p swig/java/gdal.jar  \
    %{buildroot}%{_javadir}/gdal.jar

# Install Maven pom and update version number
install -dm 755 %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE2} %{buildroot}%{_mavenpomdir}/JPP-gdal.pom
sed -i 's|<version></version>|<version>%{version}</version>|' %{buildroot}%{_mavenpomdir}/JPP-gdal.pom

# Create depmap fragment
%add_maven_depmap JPP-gdal.pom gdal.jar

# 775 on the .so?
# copy JNI libraries and links, non versioned link needed by JNI
# What is linked here?
mkdir -p %{buildroot}%{_jnidir}/gdal
# cp -pl swig/java/.libs/*.so*  \
cp -pl swig/java/.libs/*.so*  \
    %{buildroot}%{_jnidir}/gdal/
chrpath --delete %{buildroot}%{_jnidir}/gdal/*jni.so*

# Install Java API documentation in the designated place
mkdir -p %{buildroot}%{_javadocdir}/gdal
cp -pr swig/java/java/org %{buildroot}%{_javadocdir}/gdal

# Install refmans
for docdir in %{docdirs}; do
  pushd $docdir
#     path=%{_builddir}/gdal-%{version}-fedora/refman
    path=%{_builddir}/gdal-%{version}/refman
    mkdir -p $path/html/$docdir
    cp -r html $path/html/$docdir

    # Install all Refmans
    %if %{build_refman}
        if [ -f latex/refman.pdf ]; then
                mkdir -p $path/pdf/$docdir
                cp latex/refman.pdf $path/pdf/$docdir
        fi
    %endif
  popd
done

# Install formats documentation
for dir in gdal_frmts ogrsf_frmts; do
  mkdir -p $dir
  find frmts -name "*.html" -exec install -p -m 644 '{}' $dir \;
done

#TODO: Header date lost during installation
# Install multilib cpl_config.h bz#430894
install -p -D -m 644 port/cpl_config.h %{buildroot}%{_includedir}/gdal/cpl_config-%{cpuarch}.h
# Create universal multilib cpl_config.h bz#341231
# The problem is still there in 1.9.
#TODO: Ticket?

#>>>>>>>>>>>>>
cat > %{buildroot}%{_includedir}/gdal/cpl_config.h <<EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "gdal/cpl_config-32.h"
#else
#if __WORDSIZE == 64
#include "gdal/cpl_config-64.h"
#else
#error "Unknown word size"
#endif
#endif
EOF
#<<<<<<<<<<<<<
touch -r NEWS port/cpl_config.h

# Create and install pkgconfig file
#TODO: Why does that exist? Does Grass really use it? I don't think so.
# http://trac.osgeo.org/gdal/ticket/3470
#>>>>>>>>>>>>>
cat > gdal.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: GDAL
Description: GIS file format library
Version: %{version}
Libs: -L\${libdir} -lgdal
Cflags: -I\${includedir}/gdal
EOF
#<<<<<<<<<<<<<
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
install -m 644 gdal.pc %{buildroot}%{_libdir}/pkgconfig/
touch -r NEWS %{buildroot}%{_libdir}/pkgconfig/gdal.pc

# Multilib gdal-config
# Rename the original script to gdal-config-$arch (stores arch-specific information)
# and create a script to call one or the other -- depending on detected architecture
# TODO: The extra script will direct you to 64 bit libs on
# 64 bit systems -- whether you like that or not
mv %{buildroot}%{_bindir}/gdal-config %{buildroot}%{_bindir}/gdal-config-%{cpuarch}
#>>>>>>>>>>>>>
cat > %{buildroot}%{_bindir}/gdal-config <<EOF
#!/bin/bash

ARCH=\$(uname -m)
case \$ARCH in
x86_64 | ppc64 | ppc64le | ia64 | s390x | sparc64 | alpha | alphaev6 | aarch64 )
gdal-config-64 \${*}
;;
*)
gdal-config-32 \${*}
;;
esac
EOF
#<<<<<<<<<<<<<
touch -r NEWS %{buildroot}%{_bindir}/gdal-config
chmod 755 %{buildroot}%{_bindir}/gdal-config

# Clean up junk
rm -f %{buildroot}%{_bindir}/*.dox

#jni-libs and libgdal are also built static (*.a)
#.exists and .packlist stem from Perl
for junk in {*.a,*.la,*.bs,.exists,.packlist} ; do
  find %{buildroot} -name "$junk" -exec rm -rf '{}' \;
done

# Don't duplicate license files
rm -f %{buildroot}%{_datadir}/gdal/LICENSE.TXT

# Throw away random API man mages plus artefact seemingly caused by Doxygen 1.8.1 or 1.8.1.1
for f in 'GDAL*' BandProperty ColorAssociation CutlineTransformer DatasetProperty EnhanceCBInfo ListFieldDesc NamedColor OGRSplitListFieldLayer VRTBuilder; do
  rm -rf %{buildroot}%{_mandir}/man1/$f.1*
done

# Fix python interpreter
sed -i '1s|^#!/usr/bin/env python$|#!%{__python2}|' %{buildroot}%{_bindir}/*.py

# Cleanup .pyc for now
rm -f %{buildroot}%{_bindir}/*.pyc

#TODO: What's that?
# rm -f %{buildroot}%{_mandir}/man1/*_gdal-%{version}-fedora_apps_*
rm -f %{buildroot}%{_mandir}/man1/*_gdal-%{version}_apps_*
rm -f %{buildroot}%{_mandir}/man1/_home_rouault_dist_wrk_gdal_apps_.1*

%check
%if %{run_tests}
for i in -I/usr/lib/jvm/java/include{,/linux}; do
    java_inc="$java_inc $i"
done


pushd gdalautotest-%{testversion}
  # Export test enviroment
  export PYTHONPATH=$PYTHONPATH:%{buildroot}%{python_sitearch}
  #TODO: Nötig?
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{buildroot}%{_libdir}
#  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%%{buildroot}%%{_libdir}:$java_inc

  export GDAL_DATA=%{buildroot}%{_datadir}/gdal/

  # Enable these tests on demand
  #export GDAL_RUN_SLOW_TESTS=1
  #export GDAL_DOWNLOAD_TEST_DATA=1

  # Remove some test cases that would require special preparation
 rm -rf ogr/ogr_pg.py        # No database available
 rm -rf ogr/ogr_mysql.py     # No database available
 rm -rf osr/osr_esri.py      # ESRI datum absent
 rm -rf osr/osr_erm.py       # File from ECW absent

  # Run tests but force normal exit in the end
  ./run_all.py || true
popd
%endif #%%{run_tests}


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%{_sysconfdir}/bash_completion.d/gdal
%{_bindir}/gdallocationinfo
%{_bindir}/gdal_contour
%{_bindir}/gdal_rasterize
%{_bindir}/gdal_translate
%{_bindir}/gdaladdo
%{_bindir}/gdalinfo
%{_bindir}/gdaldem
%{_bindir}/gdalbuildvrt
%{_bindir}/gdaltindex
%{_bindir}/gdalwarp
%{_bindir}/gdal_grid
%{_bindir}/gdalenhance
%{_bindir}/gdalmanage
%{_bindir}/gdalserver
%{_bindir}/gdalsrsinfo
%{_bindir}/gdaltransform
%{_bindir}/nearblack
%{_bindir}/ogr*
%{_bindir}/8211*
%{_bindir}/s57*
%{_bindir}/testepsg
%{_mandir}/man1/gdal*.1*
%exclude %{_mandir}/man1/gdal-config.1*
%exclude %{_mandir}/man1/gdal2tiles.1*
%exclude %{_mandir}/man1/gdal_fillnodata.1*
%exclude %{_mandir}/man1/gdal_merge.1*
%exclude %{_mandir}/man1/gdal_retile.1*
%exclude %{_mandir}/man1/gdal_sieve.1*
%{_mandir}/man1/nearblack.1*
%{_mandir}/man1/ogr*.1*
%{_mandir}/man1/gnm*.1.*


%files libs
%doc LICENSE.TXT NEWS PROVENANCE.TXT COMMITERS
%{_libdir}/libgdal.so.*
%{_datadir}/gdal
#TODO: Possibly remove files like .dxf, .dgn, ...
%dir %{_libdir}/gdalplugins

%files devel
%{_bindir}/gdal-config
%{_bindir}/gdal-config-%{cpuarch}
%{_mandir}/man1/gdal-config.1*
%dir %{_includedir}/gdal
%{_includedir}/gdal/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/gdal.pc

# Can I even have a separate Java package anymore?
%files java -f .mfiles
%doc swig/java/apps
%{_jnidir}/gdal/

%files javadoc
%{_javadocdir}/gdal

%files perl
%doc swig/perl/README
%{perl_vendorarch}/*
%{_mandir}/man3/*.3pm*

%files python
%doc swig/python/README.txt
%doc swig/python/samples
#TODO: Bug with .py files in EPEL 5 bindir, see http://fedoraproject.org/wiki/EPEL/GuidelinesAndPolicies
%{_bindir}/*.py
%{_mandir}/man1/pct2rgb.1*
%{_mandir}/man1/rgb2pct.1*
%{_mandir}/man1/gdal2tiles.1*
%{_mandir}/man1/gdal_fillnodata.1*
%{_mandir}/man1/gdal_merge.1*
%{_mandir}/man1/gdal_retile.1*
%{_mandir}/man1/gdal_sieve.1*
%{python2_sitearch}/osgeo
%{python2_sitearch}/GDAL-%{version}-py*.egg-info
%{python2_sitearch}/osr.py*
%{python2_sitearch}/ogr.py*
%{python2_sitearch}/gdal*.py*

%files python3
%doc swig/python/README.txt
%doc swig/python3/samples
%{python3_sitearch}/osgeo
%{python3_sitearch}/GDAL-%{version}-py*.egg-info
%{python3_sitearch}/osr.py
%{python3_sitearch}/__pycache__/osr.*.py*
%{python3_sitearch}/ogr.py
%{python3_sitearch}/__pycache__/ogr.*.py*
%{python3_sitearch}/gdal*.py
%{python3_sitearch}/__pycache__/gdal*.*.py*

%files doc
%doc gdal_frmts ogrsf_frmts refman

%changelog
* Wed Jan 24 2018 Justin Bronn <justin.bronn@digitalglobe.com> - 2.1.4-2
- Link to latest libraries in EPEL, including libarmadillo.so.8
* Wed Nov 15 2017 Justin Bronn <justin.bronn@digitalglobe.com> - 2.1.4-1
- Initial Release
