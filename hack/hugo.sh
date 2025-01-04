#!/bin/bash

VERSION=$(curl --silent "https://api.github.com/repos/gohugoio/hugo/releases/latest" | jq -r .tag_name | tr -d 'v')
wget https://github.com/gohugoio/hugo/releases/download/v${VERSION}/hugo_${VERSION}_Linux-64bit.tar.gz
tar zxvf hugo_${VERSION}_Linux-64bit.tar.gz
sudo mv hugo /usr/local/bin
