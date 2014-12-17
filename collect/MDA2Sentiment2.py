from mrjob.job import MRJob

import sys
import boto

from boto.s3.key import Key
from boto.s3.bucket import Bucket
from boto.s3.connection import S3Connection

import pysentiment as ps

AWS_ACCESS = ""
AWS_SECRET = ""
BUCKET = "midsedgar"

class MDA2Sentiment2(MRJob):
    bucket = None
    hiv4 = None

    def mapper_init(self):
        sys.stderr.write("Initializing module...\n")
        self.hiv4 = ps.HIV4()
	sys.stderr.write("--> Initialized sentimentor\n")
        
    def mapper(self, _, line):
        path, tab, blob = line.partition('\t')
	path=path.replace("\"","")
        tokens = self.hiv4.tokenize(blob)
        score = self.hiv4.get_score(tokens)
        sys.stderr.write("--> Score for the filecontents are: " + str(score) + "\n\n")
        yield path, str(score)

if __name__ == '__main__':
   MDA2Sentiment2.run()

