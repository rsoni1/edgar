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

class MDA2Sentiment(MRJob):
    bucket = None
    hiv4 = None

    def mapper_init(self):
        sys.stderr.write("Initializing module...\n")
        self.hiv4 = ps.HIV4()
	sys.stderr.write("--> Initialized sentimentor\n")

        # Get S3 connection
        conn = boto.connect_s3(AWS_ACCESS, AWS_SECRET)
        self.bucket = conn.get_bucket(BUCKET)
	sys.stderr.write("--> Created AWS connection\n")
	
        
    def mapper(self, _, line):
        path, code = line.split('\t')
        cleanpath = path.replace("\"","").replace("edgar/data","extract")
        if code == "1":
            sys.stderr.write("--> Grabbing filename: " + cleanpath + " from S3\n")
            key = self.bucket.get_key(cleanpath)
            filecontents = key.get_contents_as_string()
            sys.stderr.write("--> Successfully grabbed " + cleanpath + ". The contents are --- " + filecontents[0:40] + "...\n")
            
            tokens = self.hiv4.tokenize(filecontents)
            score = self.hiv4.get_score(tokens)
            sys.stderr.write("--> Score for the filecontents are: " + str(score) + "\n\n")
            yield cleanpath, str(score)
        else:
            sys.stderr.write("--> Skipping file " + cleanpath + "because the code is: " + code + "\n")

#    def reducer(self, key, values):
#        yield key, values

if __name__ == '__main__':
   MDA2Sentiment.run()

