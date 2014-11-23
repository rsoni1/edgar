#!/bin/sh

# Author : Ritesh Soni
# Project : W205 Final project
# Usage : ./getfiling.sh
# Description : Gets the filing and extracts the MD&A section from the filing

# Edgar ftp URL for the full index
URL=ftp://ftp.sec.gov/

echo $1
filename=`basename $1`
dirname=`echo $1 |awk -F "/" '{print $3}'`
extract=`basename $1 | sed 's/\.txt/_md.txt/'`
# echo Downloading $filename $extract $dirname

[ -d "../data/$dirname" ] || mkdir ../data/$dirname

[ ! -e ../data/$dirname/$filename ] && curl $URL/$1 > ../data/$dirname/$filename




