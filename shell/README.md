# shell

Build Hootenanny RPM build container using release dependencies (those that are already available):

```
./shell/BuildHootImages
```

Once that's complete you can build a Hootenanny archive tarball with:

```
./shell/BuildArchive.sh
```

And the RPMs may be built with:

```
./shell/BuildHoot.sh
```

Note: dependency-only packages will be in `RPMS/noarch`, and Hootenanny packages will be placed in `RPMS/x86_64`.
