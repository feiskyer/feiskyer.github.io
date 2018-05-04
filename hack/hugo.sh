#!/bin/bash

go get -u -d github.com/magefile/mage
cd $GOPATH/src/github.com/magefile/mage
go run bootstrap.go
go get github.com/magefile/mage
go get -d github.com/gohugoio/hugo
cd ${GOPATH}/src/github.com/gohugoio/hugo
mage vendor
mage install

