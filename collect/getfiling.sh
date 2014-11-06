#!/bin/sh

# Author : Ritesh Soni
# Project : W205 Final project
# Usage : ./getfiling.sh
# Description : Gets the filing and extracts the MD&A section from the filing

# Edgar ftp URL for the full index
URL=ftp://ftp.sec.gov/

for filing in `cat $1`
do

	echo Downloading $filing
	filename=`basename $filing`
	dirname=`echo $filing |awk -F "/" '{print $3}'`
	# echo Downloading $filename $extract $dirname
	[ -d data/$dirname ] || mkdir data/$dirname
	[ ! -e data/$dirname/$filename ] && curl -s -S $URL/$filing > data/$dirname/$filename || echo $filing >>$1.failed 
	aws s3 cp data/$dirname/$filename s3://midsedgar/data/$dirname/$filename
	rm data/$dirname/$filename
done
