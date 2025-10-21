#!/bin/bash
rm -f .git/index.lock
git status
git add .
git commit -m "update"
git push origin main
git log --oneline --graph --decorate -n 10