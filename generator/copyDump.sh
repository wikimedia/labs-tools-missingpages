#!/bin/bash

cp `ls -d /public/dumps/public/cswiki/* | sort -n | head -n1`/cswiki-*-pages-articles.xml.bz2 .
mv cswiki-*-pages-articles.xml.bz2 cswiki-latest-pages-articles.xml.bz2
bzip2 -d cswiki-lastest-pages-articles.xml.bz2
