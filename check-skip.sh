#!/usr/bin/env bash
SKIP_VAR_NAME="found"  # variable name to set in Azure job

help () {
  echo "Search for a skip command in the commit message and set Azure variable."
  echo
  echo "Usage: check-skip.sh [merge_commit_message]"
  echo
  echo "If merge_commit_message is not provided as an argument, its value"
  echo "will be taken from a COMMIT_MESSAGE environment variable."
  echo "An alternative list of skip commands can be specified in a"
  echo "SKIP_COMMANDS environment variable as space separated commands"
  echo "with commands containing spaces inside escaped double quotes."
  echo
}

require_argument () {
  if [[ -z $2 ]]; then
    echo "Argument '$1' must be given." 1>&2
    exit 1
  fi
}

get_skip_commands () {
  if [[ -n $SKIP_COMMANDS ]]; then
    # "\"[skip ci]\" \"skip tests\" pass" -> "[skip ci]" "skip tests" "pass"
    if ! declare -a -g "SKIP_COMMANDS=($SKIP_COMMANDS)"; then
      echo "Bash version 4.2 or later required for custom skip commands." 1>&2
      exit 1
    fi
    printf "Using custom skip commands:"
  else
    SKIP_COMMANDS=(
      "[skip ci]" "[ci skip]"
      "skip-checks: true" "skip-checks:true"
      "[skip azurepipelines]" "[azurepipelines skip]"
      "[skip azpipelines]" "[azpipelines skip]"
      "[skip azp]" "[azp skip]"
      "***NO_CI***"
    )
    # https://docs.microsoft.com/en-us/azure/devops/pipelines/scripts/git-commands
    printf "Using default skip commands:"
  fi
  for c in "${SKIP_COMMANDS[@]}"; do
    printf " '%s'" "$c"
  done
  printf "\n"
}

get_merge_commit_message () {
  if [[ -n "$1" ]]; then
    MERGE_MSG=$1
  elif [[ -n "$COMMIT_MESSAGE" ]]; then
    MERGE_MSG=$COMMIT_MESSAGE
  else
    help
    exit 1
  fi
  echo "Merge commit being tested: '$MERGE_MSG'"
}

get_commit_hash () {
  require_argument merge_commit_message "$1"
  if ! [[ $1 =~ ^Merge[[:space:]][0-9a-fA-F]+[[:space:]]into[[:space:]][0-9a-fA-F]+$ ]]; then
    echo "Expected commit message to be of form 'Merge HEX into HEX'." 1>&2
    echo "Please open an issue: https://github.com/OpenAstronomy/azure-pipelines-templates/issues" 1>&2
    exit 1
  fi
  COMMIT_HASH=$(echo "$1" | awk '{print $2}')
  echo "Latest commit hash in PR branch: '$COMMIT_HASH'"
}

get_commit_message () {
  require_argument commit_hash "$1"
  if [[ -n "$PR_NUMBER" ]]; then
    echo "Fetching fork at PR #$PR_NUMBER"
    git fetch origin "refs/pull/$PR_NUMBER/head"
  fi
  MSG=$(git log --format=%B -n 1 "$1")
  if [ $? -ne 0 ]; then
    echo "Error running: git log --format=%B -n 1 $1" 1>&2
    exit 1
  fi
  MSG=$(echo "$MSG" | head -1)
  echo "Message being searched for skip commands: '$MSG'"
}

set_skip_var () {
  if ! [[ "true false" =~ (^|[[:space:]])$1($|[[:space:]]) ]]; then
    echo "Argument must be 'true' or 'false', got '$1'." 1>&2
    exit 1
  fi
  echo "##vso[task.setvariable variable=$SKIP_VAR_NAME;isOutput=true]$1"
}

search_for_skip () {
  require_argument message "$1"
  for c in "${SKIP_COMMANDS[@]}"; do
    if [[ "$1" =~ "$c" ]]; then
      echo "Found command '$c' in message."
      set_skip_var true
      exit 0
    fi
  done
  echo "No skips commands found in message."
  set_skip_var false
}

get_merge_commit_message "$1"
get_commit_hash "$MERGE_MSG"
get_commit_message "$COMMIT_HASH"
get_skip_commands
search_for_skip "$MSG"
