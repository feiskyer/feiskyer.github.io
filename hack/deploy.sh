#!/bin/bash
set -e

hexo clean
hexo generate
cd .deploy_git
rm -rf ./*
cp -r ../public/* .
git add -A .
git commit -a -m 'Site updated'
git push -q -u origin master
