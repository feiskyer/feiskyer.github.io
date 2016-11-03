#!/bin/bash
set -e

cat >> _config.yml <<EOF
deploy: 
  type: git
  branch: master
  repo: https://${GitHubKEY}@github.com/feiskyer/feiskyer.github.io.git
EOF

hexo deploy --generate
