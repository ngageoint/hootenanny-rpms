# Hootenanny RPMs

This repository houses the RPM building specifications for Hootenanny and its
third-party dependencies.

RPMs are built in minimal, ephemeral CentOS 7 Docker containers.  Invoking
programs use [`config.yml`](./docs/config.md) as the source of truth for
version information.

## Requirements

To use this repository, you'll need the following:

* RPM tools (in particular, `rpmspec`)
* Docker
* Vagrant 2.0+
* `make`

For details on how to install these requirements on a Linux machine, read the
[setup documentation](./docs/setup.md).

## Quickstart

This will build Hootenanny RPM from its
[`develop`](https://github.com/ngageoint/hootenanny/tree/develop) branch:

```
make archive
make rpm
```
## Additional Information

Consult the [documentation index](./docs) for background, configuration, and
information on additional topics.

## Licensing

Due to the inclusion of third-party source archives and `.spec` files,
and the nature of building RPMs, this repository is an aggregate work --
not everything in this repository is covered by the [GPLv3](./LICENSE).
Please consult the [provenance documentation](./docs/provenance.md)
for additional details.
