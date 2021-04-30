#!/bin/sh

#
# Custom action for Source Tree app to copy commit URL on GitHub
# Menu caption: Copy Changeset URL on GitHub
# Script to run: ~/bin/github-commit-url
# Parameters: $REPO $SHA
#

if (( $# != 2 ))
then
  echo "Usage: github-commit-url {repo-path} {sha}"
  exit 1
fi

repo=$1
sha=$2
origin=`cd $repo && git config --get remote.origin.url`

# put everything together
github_url="$origin/commit/$sha"

# replace git@ with https://
github_url=${github_url/git@/https://}

# replace github.com:username with github.com/username
github_url=${github_url/github.com:/github.com/}

# remove .git part
github_url=${github_url/.git/}

echo "REPO: $repo"
echo "SHA: $sha"

echo $github_url | pbcopy
