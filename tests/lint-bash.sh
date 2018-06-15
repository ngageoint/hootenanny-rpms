#!/bin/bash
set -euo pipefail

if [ ! -x /usr/bin/shellcheck ]; then
    echo "Linting bash scripts requires shellcheck."
    exit 1
fi

# The chosen scripts.
shellcheck \
    scripts/docker-install.sh \
    scripts/hoot-archive.sh \
    scripts/hoot-repo.sh \
    scripts/latest-archive.sh \
    scripts/query-archive.sh \
    scripts/repo-update.sh \
    scripts/rpm-install.sh \
    scripts/vagrant-install.sh

# Scripts with *only* quoting errors.
shellcheck \
    --exclude SC2086 \
    scripts/hoot-checkout.sh \
    scripts/nodejs-install.sh \
    scripts/nodesource-repo.sh \
    scripts/pgdg-repo.sh \
    scripts/postgresql-install.sh \
    scripts/repo-sign.sh \
    scripts/repo-sync.sh \
    shell/BuildArchive.sh \
    shell/BuildDeps.sh \
    shell/BuildHoot.sh \
    shell/BuildHootImages.sh \
    shell/BuildRunImages.sh

# TODO: shell/Vars.sh needs a lot of work.
shellcheck \
    --exclude SC2002,SC2005,SC2012,SC2034,SC2046,SC2086,SC2148,SC2155 \
    shell/Vars.sh

# The shellcheck doesn't like non-shell shebangs, so exclude the first
# line when running these scripts through shell check.
DUMB_INIT_FILES=(
    scripts/build-entrypoint.sh
    scripts/runtime-entrypoint.sh
)

for file in "${DUMB_INIT_FILES[@]}"; do
    length="$(wc -l "$file" | awk '{ print $1 }')"
    shellcheck \
        --shell bash --exclude SC2068,SC2086 \
        <(tail -n "$((length - 1))" "$file")
done

# Check the test scripts themselves.
shellcheck --shell bash tests/*.sh
