#!/bin/sh

# Author : Ritesh Soni
# Project : W205 Final project
# Usage : ./getindex.sh
# Description : Extracts the 10-K index files from the Edgar database

# Edgar ftp URL for the full index
URL=ftp://ftp.sec.gov/edgar/full-index

years='1994 1995 1996 1997 1998 1999 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014'
qtrs='1 2 3 4'

for year in `echo $years`
do
    for q in `echo $qtrs`
    do
	[ ! -e ../idx/$year-$q-form.idx ] && curl $URL/$year/QTR$q/form.idx | grep ^10-K\ >| ../idx/$year-$q-form.idx
    done
done

# Download the current idx
rm ../idx/2014-4-form.idx
curl $URL/2014/QTR4/form.idx | grep ^10-K\ >| ../idx/2014-4-form.idx
