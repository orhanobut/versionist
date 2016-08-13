#!/usr/bin/env bash
NOW=$(date +%F)
BRANCH_NAME="update-$NOW"

echo "Checkout master"
git checkout master

echo "Pull the latest changes from upstream"
git pull origin master

echo "$BRANCH_NAME branch is created"
git checkout -b $BRANCH_NAME

echo "Generating README"
python read_me_generator.py

echo "Committing new changes"
git add .
git commit -am "Update versions"

echo "Pushing the new branch"
git push origin $BRANCH_NAME

echo "Checkout back to master"
git checkout master

echo "Deleting the local branch"
git branch -D $BRANCH_NAME