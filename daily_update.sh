#!/usr/bin/env bash

echo "Pull the latest changes from upstream"
git pull origin master

echo "Generating README"
python3 read_me_generator.py

echo "Committing new changes"
git add .
git commit -am "Update versions"

echo "Pushing the changes"
git push origin master

