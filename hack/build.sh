#!/bin/bash
set -e

# config git
git config --global user.name "Pengfei Ni"
git config --global user.email feiskyer@gmail.com
git clone -b master https://${GitHubKEY}@github.com/feiskyer/feiskyer.github.io.git .deploy_git

# update new sites
rm -rf .deploy_git/*
hugo -b https://feisky.xyz/ -E -d .deploy_git --minify

cd .deploy_git
cat >README.md <<EOF
# 个人博客

<https://feisky.xyz>
EOF

# Update travis
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
