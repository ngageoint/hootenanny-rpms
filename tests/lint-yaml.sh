#!/bin/bash
set -euo pipefail

if [ ! -x /usr/bin/yamllint ]; then
    echo "Linting YAML files requires yamllint."
    exit 1
fi

# Check our config.yaml.
yamllint config.yml

# Check the .yamllint configuration file itself, with no customization.
yamllint -d "{extends: default, rules: {}}" .yamllint

# Check the CircleCI configuration.
if [ -f .circleci/config.yml ]; then
    yamllint .circleci/config.yml
fi

# Check the TravisCI configuration.
if [ -f .travis.yml ]; then
    yamllint .travis.yml
fi
