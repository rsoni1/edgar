#!/bin/sh

# Author : Ritesh Soni
# Project : W205 Final project
# Usage : ./getfiling.sh
# Description : Gets the filing and extracts the MD&A section from the filing

filename=`basename $1`
dirname=`echo $1 |awk -F "/" '{print $3}'`
extract=`basename $1 | sed 's/\.txt/_md.txt/'`

[ -d "../extract/$dirname" ] || mkdir ../extract/$dirname

# Extracting MDA
#cat ../data/$dirname/$filename | awk -v start='${START[0]}' -v end='${END[0]}' 'BEGIN{flag=0}
# $0 ~ start{flag=1; print $0}
#  $0 ~ end{flag=0}
#  {if (flag == 1) print $0}'

cat ../data/$dirname/$filename | 
awk 'BEGIN{flag=0}
     /^ITEM\ 7\./{flag=1}
     /^ITEM\ 7\./{flag=1}
     /^ITEM\ 7A\./{flag=0}
     /^ITEM\ 8\./{flag=0}
     {if (flag == 1) print $0}' >| ../extract/$dirname/$extract

  
