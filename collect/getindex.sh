#!/bin/sh

# Author : Ritesh Soni
# Project : W205 Final project
# Usage : ./getindex.sh
# Description : Extracts the 10-K index files from the Edgar database

# Edgar ftp URL for the full index
URL=ftp://ftp.sec.gov/edgar/full-index

years='1994 1998 2002 2006 2010 2014'
qtrs='1'

for year in `echo $years`
do
    for q in `echo $qtrs`
    do
	[ ! -e ../idx/$year-$q-form.idx ] && curl $URL/$year/QTR$q/form.idx | grep ^10-K\ >| ../idx/$year-$q-form.idx
    done
done

