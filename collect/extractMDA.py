from mrjob.job import MRJob
from boto.s3.key import Key
from boto.s3.bucket import Bucket
import boto
import random
import os, sys, commands, shutil

AWS_ACCESS = ""
AWS_SECRET = ""
BUCKET = "midsedgar"
MDA_THRESHOLD = 1000
PERL_CODE_KEY = "extract.pl"

class MRExtractMDA(MRJob):
    bucket = None

    def mapper_init(self):
        sys.stderr.write("Initializing connection...\n")
        # Get S3 connection
        conn = boto.connect_s3(AWS_ACCESS, AWS_SECRET)
        self.bucket = conn.get_bucket(BUCKET)
        # Copy the Perl code locally
        key = self.bucket.get_key(PERL_CODE_KEY)
        f = open('/tmp/'+PERL_CODE_KEY,'w')
        key.get_contents_to_file(f)
        f.close()
        
    def mapper(self, _, line):
        # extract key from input line
        key_name = line[6:]
        key = self.bucket.get_key(key_name)
        # Create a tmp filename with prefix /tmp/edgar
        str='%030x' % random.randrange(16**30)
        tmp_fname = '/tmp/edgar'+str[0:8]
        f = open(tmp_fname,'w')
        # Download S3 data to local file
        key.get_contents_to_file(f)
        f.close()

        # Extract MDA
        respond=commands.getoutput("perl /tmp/extract.pl "+tmp_fname)
        mda_file = tmp_fname+'_mda'
        if "mda outputted" in respond:
            # Check if the filesize is above threshold
            sys.stderr.write("Processing "+tmp_fname+"\n")
            statinfo = os.stat(mda_file)
            size = statinfo.st_size
            if (size > MDA_THRESHOLD):
                # Save extract in S3
                mda_key = "extract/"+line[11:]
                k = Key(self.bucket)
                k.key = mda_key
                k.set_contents_from_filename(mda_file)
                self.increment_counter('extract','success',1)
                yield line, 1
            else:
                self.increment_counter('extract','limited',1)                
                yield line, 2
        else:
            self.increment_counter('extract','failed',1)                
            yield line, -1
        
        # Cleanup tmp
        for file in [f for f in os.listdir("/tmp") if f.startswith("edgar")]:
            os.remove("/tmp/"+file)

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
   MRExtractMDA.run()

