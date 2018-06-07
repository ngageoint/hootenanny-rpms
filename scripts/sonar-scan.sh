#!/bin/bash
set -euo pipefail

# Defaults.
USAGE=no
SONAR_BRANCH=""
SONAR_EXCLUSIONS="**/*.pb.cc,**/*.pb.h,**/*.sql"
SONAR_GITHUB_OAUTH=""
SONAR_GITHUB_PULL=""
SONAR_GITHUB_REPO=""
SONAR_HOST_URL="https://sonarcloud.io"
SONAR_LOGIN=""
SONAR_ORG=""
SONAR_PROJECT=""
SONAR_SOURCES="./hoot-core,./hoot-js,./hoot-rnd,./tbs,./tgs"
SONAR_THREADS="$(nproc)"

# Getting parameters from the command line.
while getopts ":a:b:j:l:o:p:r:s:t:" opt; do
    case "$opt" in
        # Required parameters.
        a)
            SONAR_GITHUB_OAUTH="$OPTARG"
            ;;
        b)
            SONAR_BRANCH="$OPTARG"
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
    echo "sonar-scan.sh:"
    echo "  -l <Sonar Login token>"
    echo "  -o <Sonar Organization>"
    echo "  -r <GitHub Repository>"
    echo "  -j <Sonar Project>"
    echo " [-a <Sonar GitHub OAuth>]"
    echo " [-b <Sonar Branch Name>]"
    echo " [-p <Sonar GitHub PR>]"
    echo " [-s <Sonar Sources>]"
    echo " [-t <Sonar Threads>]"
    exit 1
}

# Abort if invalid options.
if [[ "$USAGE" = "yes" || -z "$SONAR_LOGIN" || -z "$SONAR_ORG" || -z "$SONAR_GITHUB_REPO" || -z "$SONAR_PROJECT" ]]; then
    usage
fi

# Build out the scan command options.
OPTIONS=(
    "-Dsonar.login=$SONAR_LOGIN"
    "-Dsonar.organization=$SONAR_ORG"
    "-Dsonar.github.repository=$SONAR_GITHUB_REPO"
    "-Dsonar.projectKey=$SONAR_PROJECT"
    "-Dsonar.cfamily.build-wrapper-output=bw-output"
    "-Dsonar.cfamily.lcov.reportsPaths=$HOOT_HOME"
    "-Dsonar.cfamily.threads=$SONAR_THREADS"
    "-Dsonar.exclusions=$SONAR_EXCLUSIONS"
    "-Dsonar.host.url=$SONAR_HOST_URL"
    "-Dsonar.sources=$SONAR_SOURCES"
)

# Optional scan parameters based off parameters passed into script
if [ -n "$SONAR_BRANCH" ]; then
    OPTIONS=(
        "${OPTIONS[@]}"
        "-Dsonar.branch.name=$SONAR_BRANCH"
    )
fi

if [ -n "$SONAR_GITHUB_PULL" ]; then
    # Optional pull request number that will match scan with git hub pull-request
    OPTIONS=(
        "${OPTIONS[@]}"
        "-Dsonar.github.pullRequest=$SONAR_GITHUB_PULL"
        "-Dsonar.analysis.mode=preview"
    )
fi

if [ -n "$SONAR_GITHUB_OAUTH" ]; then
    # Optional token to allow scan to post comments to github ticket
    OPTIONS=(
        "${OPTIONS[@]}"
        "-Dsonar.github.oauth=$SONAR_GITHUB_OAUTH"
    )
fi

sonar-scanner "${OPTIONS[@]}"
