#! /usr/bin/env sh

git diff --name-only HEAD~1 | xargs dirname | sort | uniq