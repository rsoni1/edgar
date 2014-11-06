#!/bin/bash

rm spfl*

# Get the latest completion status
aws s3 ls --recursive s3://midsedgar/data/ >|s3files
cat s3files | awk '{if ($3!=0) print $4}'|sed 's/^/edgar\//'|sort >|s3complete

# Calculate pending
comm -13  s3complete filings.idx >|pending.idx

# Split pending
split -l 1000 pending.idx spfl

# Start the job
for i in `ls spfl*`; do ./getfiling.sh $i& done

