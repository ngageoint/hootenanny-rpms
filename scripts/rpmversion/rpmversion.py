#!/usr/bin/env python

import argparse
import os
import sys
import yaml

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Get RPM version from YAML file for given package name.'
    )

    parser.add_argument(
        'package',
        action='store',
        help='Package key to query for in the RPM file.',
        type=str
    )

    parser.add_argument(
        '-c', '--config-file',
        action='store',
        default='config.yml',
        help='Path to YAML config file, defaults to config.yml',
        type=str
    )

    parser.add_argument(
        '--release-only',
        action='store_true',
        default=False,
        help='Output the package release only, excluding the version.'
    )

    parser.add_argument(
        '--version-only',
        action='store_true',
        default=False,
        help='Output the package version only, excluding the release.'
    )

    args = parser.parse_args()

    # Ensure YAML config file is present.
    if not os.path.isfile(args.config_file):
        sys.stderr.write('Invalid YAML configuration file.\n')
        sys.exit(os.EX_NOINPUT)

    # Open YAML file, and read out the document into `config_data` variable.
    with open(args.config_file, 'rb') as fh:
        config_data = yaml.load(fh.read())

    # Ensure that `versions` key exists in `config_data`.
    if not 'versions' in config_data:
        sys.stderr.write('No versions hash in YAML file.\n')
        sys.exit(os.EX_CONFIG)

    # Getting the package version from the versions hash.
    versions = config_data['versions']
    if not args.package in versions:
        sys.stderr.write('%s: package not in YAML versions hash.\n' % args.package)
        sys.exit(os.EX_DATAERR)
    else:
        package_version = versions[args.package]

    # Determine what the output should be.
    if args.release_only:
        output = package_version.split('-')[1]
    elif args.version_only:
        output = package_version.split('-')[0]
    else:
        output = package_version

    # Write desired information to stdout and exit.
    sys.stdout.write('%s\n' % output)
    sys.exit(os.EX_OK)
