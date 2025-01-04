#!/bin/bash

VERSION=$(curl -sSI https://github.com/gohugoio/hugo/releases/latest | awk -F "/" '/location/{print $NF}' | tr -d 'v')
wget https://github.com/gohugoio/hugo/releases/download/v${VERSION}/hugo_${VERSION}_Linux-64bit.tar.gz
tar zxvf hugo_${VERSION}_Linux-64bit.tar.gz
sudo mv hugo /usr/local/bin
