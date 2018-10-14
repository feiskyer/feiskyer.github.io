#!/bin/bash

VERSION="0.49.2"
wget https://github.com/gohugoio/hugo/releases/download/v${VERSION}/hugo_${VERSION}_Linux-64bit.tar.gz
tar zxvf hugo_${VERSION}_Linux-64bit.tar.gz
mv hugo /usr/local/bin

