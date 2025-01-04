#!/bin/bash
set -o nounset
set -o errexit
set -o pipefail

REPO_ROOT=$(realpath "$(dirname "${BASH_SOURCE}")/..")

# config git
git config --global user.name "Pengfei Ni"
git config --global user.email feiskyer@gmail.com
git clone -b master https://feiskyer:${GITHUB_TOKEN}@github.com/feiskyer/feiskyer.github.io.git ${REPO_ROOT}/.deploy_git

# update new sites
hugo -b https://feisky.xyz/ -E -d ${REPO_ROOT}/.deploy_git --minify

cd ${REPO_ROOT}/.deploy_git
cat >README.md <<EOF
# 个人博客

<https://feisky.xyz>
EOF

cat >Gemfile <<EOF
source 'https://rubygems.org'

gem 'github-pages'
EOF

# push new sites
git add -A .
git commit -a -m 'Site updated'
git push -q -u origin master
