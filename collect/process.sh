#!/bin/sh

# Author : Ritesh Soni
# Project : W205 Final project
# Usage : ./process.sh
# Description : Master extraction process

# set environment
. setenv.sh

# Create data directories if they don't exist
[ -d "../data" ] || mkdir ../data
[ -d "../extract" ] || mkdir ../extract
[ -d "../idx" ] || mkdir ../idx


# Download the index files
echo "Downloading indexes..."
./getindex.sh
echo "Downloading indexes...Done"

# Randomly extract N records from each index file to build the filings file
echo "Selecting random filings from each index"
if [ ! -e filings.idx ]
then
    >| filings.idx
    for file in `ls ../idx/*form.idx`
    do
	echo $file
	sort -R $file | head -2 >> filings.idx
    done
fi

# Download the filings
for filing in `awk '{print $NF}' filings.idx`
do
    ./getfiling.sh $filing
done

# Extract the MD&A
for filing in `awk '{print $NF}' filings.idx`
do
    #./extractmda.sh $filing
    perl extract.pl $filing
done
