# Setup

In order to generate Hootenanny RPMs, you'll need RPM tools, Docker, Vagrant,
and `make`.  Fortunately, scripts are included to automate the setup process
for Linux users.  The scripts assume:

* You're running a RedHat or Debian based distribution (e.g., CentOS and Ubuntu
  are supported).
* The Linux user running the script can use `sudo` without a password.

Note: The legacy scripts in [`shell`](./shell.md) can be used to build
Hootenanny RPMs without Vagrant or `make`, but is reserved for
resource-constrained environments.

## RPM Tools

RPM tools (including `rpmbuild` and `rpmspec`) may be installed with:

```
./scripts/rpm-install.sh
```

RPM authoring tools are required to use this repository; in particular,
`rpmspec` is required to properly parse requirements directly from `spec`
files.

## Docker

[Docker](https://docs.docker.com/) may be installed by running:

```
./scripts/docker-install.sh
```

Docker is a program for managing Linux containers.
Hootenanny and its dependencies use Docker to build RPMs in a minimal
and reproducible CentOS environments.

## Vagrant

[Vagrant](https://www.vagrantup.com/downloads.html) may be installed by running:

```
./scripts/vagrant-install.sh
```

Vagrant (version 2.0 or newer) is required to build the Docker containers.
Vagrant's [Docker provider](https://www.vagrantup.com/docs/docker/basics.html)
is used to build the Hootenanny containers and automatically handles file sharing
constructing `rpmbuild` commands.

## `make`

Make can be installed from your package manager:

```
# Debian/Ubuntu
sudo apt-get -y install make
# RedHat/CentOS
yum install -y make
```

Make is used to manage the dependency graph between containers.
In particular, some containers depend on RPMs built from different containers.
For example, `rpmbuild-gdal` requires the GEOS RPM produced from
`rpmbuild-geos`.
