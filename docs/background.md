# Background

## RPMs and Yum

[RPM](http://rpm.org) (RPM Package Manager) is a package distribution system for
Enterprise Linux platforms.  RPM packages comprise metadata and a payload of files
as a GNU gzip-compressed [`cpio`](https://en.wikipedia.org/wiki/Cpio) archive.

RPMs are created from instructions housed in a `.spec` file, typically kept
in a [`SPECS`](../SPECS) folder.  The spec file has instructions on how to
compile the package from a source archive, typically from the
[`SOURCES`](../SOURCES) folder.  The `rpmbuild` program will extract the
source archive and compile the program in a chroot-like environment and
assemble the output into `.rpm` files placed in a `RPMS` folder.

[Yum](http://yum.baseurl.org/) (Yellowdog Updater Modified) manages RPMs of
a system from a network-based repository.  It handles RPM distribution,
updates, and dependency resolution for a Enterprise Linux system.  Yum
repositories are created and updated with the `createrepo` command, and
then distributed to a webserver.

## Repository Dependencies

Building and installing Hootenanny requires the following package
repositories for dependencies:

* EPEL
* PGDG (PostgreSQL)
* Hootenanny Dependencies

### EPEL

[EPEL](https://fedoraproject.org/wiki/EPEL) (Extra Packages for Enterprise Linux),
is necessary for libraries not included in Enterprise Linux base distributions.
Both PGDG and Hootenanny packages have dependencies in the EPEL repository.

### PGDG

[PGDG](https://yum.postgresql.org/) (PostgreSQL Global Development Group) is
for stable PostgreSQL releases with newer versions than what's in the base.
While Hootenanny currently uses PostgreSQL 9.5, PGDG also provides repositories
for 9.6 and 10.0 versions.

### Hootenanny Dependencies

Hootenanny dependencies are created from the files in this repository.
While the dependencies can be compiled from source, a set of stable
dependencies are signed and kept in a *release* repository published on S3.
