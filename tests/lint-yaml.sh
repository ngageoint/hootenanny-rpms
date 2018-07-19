#!/bin/bash
# Copyright (C) 2018 Radiant Solutions (http://www.radiantsolutions.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
