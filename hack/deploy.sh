#!/bin/bash
set -e

# generate sites
hexo clean
hexo generate

# config git
git config --global user.name "Pengfei Ni"
git config --global user.email feiskyer@gmail.com
git clone -b master https://${GitHubKEY}@github.com/feiskyer/feiskyer.github.io.git .deploy_git

# update new sites
cd .deploy_git
rm -rf ./*
cp -r ../public/* .
cp ../README.md .
cat >Gemfile <<EOF
source 'https://rubygems.org'

gem 'github-pages'
EOF
cat >.travis.yml <<EOF
language: ruby

rvm:
- 2.1

script: "bundle exec jekyll build"
EOF

# push new sites
git add -A .
git commit -a -m 'Site updated'
git push -q -u origin master
