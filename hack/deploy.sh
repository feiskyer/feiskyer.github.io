#!/bin/bash
set -e

# generate sites
hexo clean
hexo generate

# config git
git config --global user.name "Pengfei Ni"
git config --global user.email feiskyer@gmail.com
git clone -b master https://${GitHubKEY}@github.com/feiskyer/feiskyer.github.io.git .deploy_git

# push new sites
cd .deploy_git
rm -rf ./*
cp -r ../public/* .
git add -A .
git commit -a -m 'Site updated'
git push -q -u origin master
