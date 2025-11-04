#!/usr/bin/env bash
rm -f .git/index.lock
git fetch --all
git status
git pull origin main
git log --oneline --graph --decorate -n 10
