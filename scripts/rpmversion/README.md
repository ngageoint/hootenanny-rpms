# `rpmversion`

This is to provide a binary that embeds a script to spit out the desired version value from `config.yml`.

## Requirements

* Python 2 (because it's available in bare CentOS install)
* PEX

## Building

From this directory you can re-build the `rpmversion` binary with the following:

```
pex . -c rpmversion.py -o ../../rpmversion
```
