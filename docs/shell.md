# shell

Scripts in the [`shell`](../shell) directory can be used to build the RPMs
on constrained systems without Vagrant or `make`.

## Usage

Use the following to build Hootenanny RPMs:

1. First build the required Hootenanny containers:

   ```
   ./shell/BuildHootImages.sh
   ```

1. Next, create the Hootenanny source archive:

   ```
   ./shell/BuildArchive.sh
   ```

1. Finally, create the RPMs:

   ```
   ./shell/BuildHoot.sh
   ```

## Reference

### Scripts

* [`BuildArchive.sh`](./BuildArchive.sh):  Builds a Hootenanny source
  code archive.
* [`BuildDeps.sh`](./BuildDeps.sh): Builds *all* Hootenanny dependency RPMs.
* [`BuildHootImages.sh`](./BuildHootImages.sh): Builds the containers
  necessary to compile Hootenanny.
* [`BuildHoot.sh`](./BuildHoot.sh): Builds Hootenanny RPMs; requires a sourc
  archive to be generated first.
* [`BuildRunImages.sh`](./BuildRunImages.sh): Builds runtime Hootenanny
  containers.
* [`Vars.sh`](./Vars.sh): Holds common variables and functions used by
  the other scripts.

### Functions

These shell functions are what power the scripts; they can be exposed
in your session by running `source shell/Vars.sh`.  The most important
are:

* `build_base_images`: Builds the base images required by the
  Hootenanny build container.
* `run_dep_image`: Runs a dependency image (defaults to `rpmbuild-generic`)
  for creating dependency RPMs.
* `run_hoot_build_image`: Runs the Hootenanny build image, used for creating
  source archives and RPMs.
