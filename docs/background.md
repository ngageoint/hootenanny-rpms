# Background

## RPMs and Yum

[RPM](http://rpm.org) (RPM Package Manager) is a package distribution system for
Enterprise Linux platforms.  RPM packages comprise metadata and a payload of files
as a GNU gzip-compressed [`cpio`](https://en.wikipedia.org/wiki/Cpio) archive.

RPMs are created from instructions housed in a `.spec` file, typically kept
in a [`SPECS`](../SPECS) folder.  The spec file has instructions on how to
compile and patch the program from a source archive, typically in the
[`SOURCES`](../SOURCES) folder.  The `rpmbuild` program will extract the
source archive and compile the program in a chroot-like environment and
assemble the output into `.rpm` files placed in a `RPMS` folder.

[Yum](http://yum.baseurl.org/) (Yellowdog Updater Modified) manages RPMs of
a system from a network-based repository.  It handles RPM distribution,
updates, and dependency resolution for a Enterprise Linux system.  Yum
repositories are created and updated with the
[`createrepo`](http://createrepo.baseurl.org/) command.  A Yum repository
consists of RPMs and metadata files (as XML and SQLite).  Once updated,
a repository is distributed to a network distribution point like a
web server or S3 bucket.

## Versioning

This repository tries to follow [Fedora's package versioning guidelines](https://fedoraproject.org/wiki/Packaging:Versioning).
In practice, this means that non-release versions will use a prerelease
version number.  For example having a `HOOT_VERSION_GEN` of
`0.2.41_2_g4d31c87` would create an RPM like `0.2.42-0.2.20180710.4d31c87`
as the version.  Specifically, the subminor version number is incremented
by one to `42` and the `Release` value is indicated as a *prerelease*
by starting with `0`.  The snapshot date (`20180710`), and the
git revision (`4d31c87`) are also included as well providing further
details about the prerelease.

For tagged releases, however, the `Release` value defaults to `1`.
Thus, a `HOOT_VERSION_GEN` of `0.2.41` would produce an RPM version
of `0.2.41-1`.

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


