#!/bin/bash
set -euo pipefail

# Defaults.
USAGE=no
SONAR_LOGIN=""
SONAR_ORG=""
SONAR_EXCLUSIONS="**/*.pb.cc,**/*.pb.h,**/*.sql"
SONAR_GITHUB_OAUTH=""
SONAR_GITHUB_PULL=""
SONAR_GITHUB_REPO=""
SONAR_HOST_URL="https://sonarcloud.io"
SONAR_PROJECT=""
SONAR_SOURCES="./hoot-core,./hoot-js,./hoot-rnd,./tbs,./tgs"
SONAR_THREADS="$(nproc)"

# Getting parameters from the command line.
while getopts ":a:l:o:r:s:t:" opt; do
    case "$opt" in
        # Required parameters.
        a)
            SONAR_GITHUB_OAUTH="$OPTARG"
            ;;
        j)
            SONAR_PROJECT="$OPTARG"
            ;;
        l)
            SONAR_LOGIN="$OPTARG"
            ;;
        o)
            SONAR_ORG="$OPTARG"
            ;;
        p)
            SONAR_GITHUB_PULL="$OPTARG"
            ;;
        r)
            SONAR_GITHUB_REPO="$OPTARG"
            ;;
        s)
            SONAR_SOURCES="$OPTARG"
            ;;
        t)
            SONAR_THREADS="$OPTARG"
            ;;
        *)
            USAGE=yes
            ;;
    esac
done
shift $((OPTIND-1))

# Setting up.
function usage() {
    echo "sonar-build.sh: You've messed up, cowboy."
    exit 1
}

# Abort if invalid options.
if [[ "$USAGE" = "yes" || -z "$SONAR_LOGIN" || -z "$SONAR_ORG" || -z "$SONAR_GITHUB_REPO" || -z "$SONAR_PROJECT" ]]; then
    usage
fi

# Configure hoot's autoconf
aclocal && autoconf && autoheader && automake --add-missing --copy
./configure --quiet --with-rnd --with-services --with-uitests

# Make with the sonar build watcher
build-wrapper-linux-x86-64 --out-dir bw-output make -sj"$SONAR_THREADS"

# Build out the scan command
CMD="sonar-scanner"
CMD+=" -Dsonar.projectKey=$SONAR_PROJECT"
CMD+=" -Dsonar.sources=$SONAR_SOURCES"
CMD+=" -Dsonar.cfamily.build-wrapper-output=bw-output"
CMD+=" -Dsonar.host.url=$SONAR_HOST_URL"
CMD+=" -Dsonar.cfamily.threads=$SONAR_THREADS"
CMD+=" -Dsonar.exclusions=$SONAR_EXCLUSIONS"
CMD+=" -Dsonar.cfamily.lcov.reportsPaths=$HOOT_HOME"
CMD+=" -Dsonar.login=$SONAR_LOGIN"
CMD+=" -Dsonar.organization=$SONAR_ORG"
CMD+=" -Dsonar.github.repository=$SONAR_GITHUB_REPO"

# Optional scan parameters based off parameters passed into script
if [ -n "$SONAR_BRANCH" ]; then
    CMD+=" -Dsonar.branch.name=$SONAR_BRANCH"
fi

if [ -n "$SONAR_GITHUB_PULL" ]; then
    # Optional pull request number that will match scan with git hub pull-request
    CMD+=" -Dsonar.github.pullRequest=$SONAR_GITHUB_PULL"
    CMD+=" -Dsonar.analysis.mode=preview"
fi

if [ -n "$SONAR_GITHUB_OAUTH" ]; then
    # Optional token to allow scan to post comments to github ticket
    CMD+=" -Dsonar.github.oauth=$SONAR_GITHUB_OAUTH"
fi

exec "$CMD"