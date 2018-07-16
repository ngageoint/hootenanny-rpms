# Setup

In order to generate Hootenanny RPMs, you'll need RPM tools, Docker, Vagrant, and `make`.
Fortunately, scripts are included to automate the setup process for Linux users.
The scripts assume:

* You're running a RedHat or Debian based distribution (e.g., CentOS and Ubuntu are supported).
* The Linux user running the script can use `sudo` without a password.

## RPM Tools

RPM authoring tools are required to use this repository.
In particular, `rpmspec` is required to properly parse requirements directly from `spec` files.
RPM tools may be installed by running:

```
./scripts/rpm-install.sh
```

## Docker

[Docker](https://docs.docker.com/) is a program for managing Linux containers.
Hootenanny and its dependencies leverage Docker to build RPMs in a minimal
and reproducible CentOS environment.  It may be installed by running:

```
./scripts/docker-install.sh
```

## Vagrant

[Vagrant](https://www.vagrantup.com/downloads.html) (version 2.0 or newer) is required to
build the Docker containers.  Vagrant's [Docker provider](https://www.vagrantup.com/docs/docker/basics.html)
is used to build the Hootenanny containers and automatically handles file sharing
constructing `rpmbuild` commands.  Vagrant may be installed by running:

```
./scripts/docker-install.sh
```

## `make`

The venerable `make` program is used to manage the dependency graph between containers.
In particular, some containers depend on RPMs built from different containers -- for example,
`rpmbuild-gdal` requires the GEOS RPM produced from the `rpmbuild-geos`.  It can be installed
with:

```
# Debian/Ubuntu
sudo apt-get -y install make
# RedHat/CentOS
yum install -y make
```
