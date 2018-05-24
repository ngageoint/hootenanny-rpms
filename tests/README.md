# Hootenanny RPMs Tests

This folder is for scripts for testing the functionality of this repository.
All tests assume being run from the repository root (the parent directory)
and are shell scripts that exit with a non-zero value on failure.

## Linting Tests

### [`lint-yaml.sh`](./lint-yaml.sh)

Runs [`yamllint`](https://yamllint.readthedocs.io/en/stable/) on:

* [`config.yml`](../config.yml
* [`.yamllint`](../.yamllint), which controls configuration of `yamllint` itself
* CI configuration files if they exist, e.g., `.travis.yml` and `.circleci/config.yml`

### [`lint-bash.sh`](./lint-bash.sh)

Runs [`shellcheck`](https://github.com/koalaman/shellcheck) on the bash scripts in:

* [`scripts/`](../scripts)
* [`shell/`](../shell)
* [`tests/](./) (the test scripts themselves)

Although the goal is to have no warnings, exceptions have been grandfathered
in for specific files and will be fixed later.
