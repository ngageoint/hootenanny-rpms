# Hootenanny RPMs

This repository houses the RPM building specifications for Hootenanny and its
third-party dependencies.

RPMs are built in minimal, ephemeral CentOS 7 Docker containers.  Invoking programs
use [`config.yml`](./config.yml) as the source of truth for version information.

## Requirements

* `rpmspec`: required to properly parse `spec` files properly so that
  containers may get their package requirements directly from the spec
  files
  * CentOS:
    ```
    sudo yum install -y rpm-build
    ```
  * Ubuntu:
    ```
    sudo apt-get -y install rpm
    ```
* Docker
* Vagrant
* `make`

## Quickstart

This will build Hootenanny RPM from `develop`:

```
make hoot-archive
make hoot-rpm
```

Note: it's common for the `hoot-archive` target to fail the first time due to
maven downloading outside dependencies.

## shell

Scripts in the [`shell`](./shell) directory can be used to build the RPMs
on constrained systems without Vagrant.
