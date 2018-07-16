# Hootenanny RPMs

This repository houses the RPM building specifications for Hootenanny and its
third-party dependencies.

RPMs are built in minimal, ephemeral CentOS 7 Docker containers.  Invoking programs
use [`config.yml`](./docs/config.md) as the source of truth for version information.

## Requirements

To use this repository, you'll need the following:

* RPM tools (in particular, `rpmspec`)
* Docker
* Vagrant 2.0+
* `make`

For details on how to install these requirements on a Linux machine, read the [setup documentation](./docs/setup.md).

## Quickstart

This will build Hootenanny RPM from `develop`:

```
make archive
make rpm
```

## shell

Scripts in the [`shell`](./shell) directory can be used to build the RPMs
on constrained systems without Vagrant.
