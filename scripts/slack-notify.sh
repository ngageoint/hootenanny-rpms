#!/bin/bash
set -euo pipefail

# Defaults.
SLACK_METHOD="https://slack.com/api/chat.postMessage"
SLACK_CHANNEL=""
SLACK_MESSAGE=""
SLACK_TOKEN=""
SLACK_USERNAME="bot"
USAGE="no"

# Retrieving command-line options.
while getopts ":c:m:t:u:" opt; do
    case "$opt" in
        c)
            SLACK_CHANNEL="$OPTARG"
            ;;
        m)
            SLACK_MESSAGE="$OPTARG"
            ;;
        t)
            SLACK_TOKEN="$OPTARG"
            ;;
        u)
            SLACK_USERNAME="$OPTARG"
            ;;
        *)
            USAGE=yes
            ;;
    esac
done
shift $((OPTIND-1))

# Document the usage for this script.
function usage() {
    echo "slack-notify.sh -c <Slack Channel> -m <Slack Message> -t <Slack Token>"
    echo "  [ -u <Slack Username> ]"
    echo ""
    echo "  Sends a text notification to the given Slack channel."
    exit 1
}

if [ -z "$SLACK_CHANNEL" -o -z "$SLACK_MESSAGE" -o -z "$SLACK_TOKEN" ]; then
    USAGE=yes
fi

if [ "$USAGE" = "yes" ]; then
    usage
fi

# Use cURL's `--form` option to automatically set to POST and use the proper
# content type.
curl \
    --form channel="$SLACK_CHANNEL" \
    --form text="$SLACK_MESSAGE" \
    --form token="$SLACK_TOKEN" \
    --form username="$SLACK_USERNAME" \
    --show-error \
    --silent \
    "$SLACK_METHOD"
