from mrjob.job import MRJob

import boto
import sys

from boto.s3.key import Key
from boto.s3.bucket import Bucket
from boto.s3.connection import S3Connection

AWS_ACCESS = ""
AWS_SECRET = ""
BUCKET = "midsedgar"

class MDA2Hdfs(MRJob):
    bucket = None

    def mapper_init(self):
        sys.stderr.write("Initializing module...\n")

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
            data = filecontents.replace('\n',' ')            
            yield cleanpath, data
        else:
            sys.stderr.write("--> Skipping file " + cleanpath + "because the code is: " + code + "\n")

#    def reducer(self, key, values):
#        yield key, values

if __name__ == '__main__':
   MDA2Hdfs.run()

