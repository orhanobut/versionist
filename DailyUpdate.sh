#!/usr/bin/env bash
NOW=$(date +%F)
BRANCH_NAME="update-$NOW"
git checkout master
git pull origin master

echo "$BRANCH_NAME branch is created"
git checkout -b $BRANCH_NAME

echo "ReadMeGenerator is running"
python ReadMeGenerator.py

echo "Committing new changes"
git add .
git commit -am "Update versions"

echo "Pushing the new branch, delete the local"
git push origin $BRANCH_NAME
git checkout master
git branch -D $BRANCH_NAME