# Hootenanny RPMs Tests

This folder is for scripts for testing the functionality of this repository.
All tests assume being run from the repository root (the parent directory)
and are shell scripts that exit with a non-zero value on failure.

## Linting Tests

### [`lint-yaml.sh`](../tests/lint-yaml.sh)

Runs [`yamllint`](https://yamllint.readthedocs.io/en/stable/) on:

* [`config.yml`](../config.yml)
* [`.yamllint`](../.yamllint), which controls configuration of `yamllint` itself
* CI configuration files if they exist, e.g., `.travis.yml` and `.circleci/config.yml`

### [`lint-bash.sh`](../tests/lint-bash.sh)

Runs [`shellcheck`](https://github.com/koalaman/shellcheck) on the bash scripts in:

* [`scripts/`](../scripts)
* [`shell/`](../shell)
* [`tests/`](../tests) (the test scripts themselves)

Although the goal is to have no warnings, exceptions have been grandfathered
in for some scripts to be fixed later.

## RPM Tests

These tests go through the RPM creation process, with a focus on creating
the latest source archives and RPMs from Hootenanny's
[`develop`](https://github.com/ngageoint/hootenanny/tree/develop) branch
and uploading them to the [S3 development repository](./install.md#development).

The following environment variables may be used to modify the test
behavior.  For example, it's common to set `REPO_PREFIX=el7/develop-test`
so that the current S3 repository at `el7/develop` is not modified
when adding new RPM tests.  CircleCI's AWS user requires access to
all S3 buckets and prefixes if they're modified.

* `ARCHIVE_BUCKET`: S3 bucket to query for Hootenanny source archive,
  defaults to `hoot-archives`.
* `ARCHIVE_PREFIX`: S3 bucket prefix for Hootenanny source archives,
  defaults to `circle/develop` (Hootenanny branch name).
* `REPO_BUCKET`: The S3 bucket to place yum repositories, defaults
  to `hoot-repo`.
* `REPO_PREFIX`: S3 bucket prefix for yum repository, defaults to
  `el7/develop`.

### [`create-rpm.sh`](../tests/create-rpm.sh)

This will create a Hootenanny RPM from the latest source archive if
it doesn't already exist in the S3 repository.  The RPM is created
using the [shell](./shell.md) scripts using the latest
[`rpmbuild-hoot-release`](https://hub.docker.com/r/hootenanny/rpmbuild-hoot-release/)
image from the Docker Hub.

### [`install-rpm.sh`](../tests/install-rpm.sh)

This ensures that the RPMs generated from `create-rpm.sh` can be
installed on the latest
[`run-hoot-release`](https://hub.docker.com/r/hootenanny/run-hoot-release/)
image from the Docker Hub.

### [`upgrade-rpm.sh`](../tests/upgrade-rpm.sh)

This test installs the latest RPM from the develop repository
and ensures the upgrade process works by installing the more
recent RPMs from `create-rpm.sh` on the
[`run-hoot-release`](https://hub.docker.com/r/hootenanny/run-hoot-release/)
image from the Docker Hub.

### [`update-sync-repo.sh`](../tests/update-sync-repo.sh)

This test will update the S3 repository with the RPMs created
by `create-rpm.sh`, pruning the oldest release in the process
(10 RPM releases are kept in the repository). A Slack notification
is sent upon successful update.
