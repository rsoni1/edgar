start:
	aws s3 cp bootstrap-mrjob.sh s3://midsedgar/bootstrap-mrjob.sh
	aws s3 cp extract.pl s3://midsedgar/extract.pl
	aws emr create-cluster --ami-version 3.2.3 --ec2-attributes KeyName=midsw205_1 --instance-groups InstanceGroupType=MASTER,InstanceCount=1,InstanceType=m1.medium InstanceGroupType=CORE,InstanceCount=10,InstanceType=m1.medium --name "mrjob Test Cluster" --log-uri s3://midsedgar/logs/ --enable-debugging --tags Name=emr --bootstrap-actions Path=s3://midsedgar/bootstrap-mrjob.sh,Name="Setup mrjob / MDA Extract" | python clusterid.py >|clusterid

status:
	aws emr list-clusters --active
	# aws emr describe-cluster --cluster-id `cat clusterid`
	aws emr list-steps --cluster-id `cat clusterid`
stop:
	aws emr terminate-clusters --cluster-id `cat clusterid`

sentiment:
	python MDA2Sentiment.py -c mrjob.conf -r emr  --emr-job-flow-id=`cat clusterid` --output-dir=s3://midsedgar/sentiment/output/ --no-output s3://midsedgar/sentiment/input/ 
	# python extractMDA.py -c mrjob.conf -r emr  --emr-job-flow-id=`cat clusterid` --output-dir=s3://midsedgar/extract1/output/ --no-output s3://midsedgar/extract1/input/ --hadoop-arg='-inputformat org.apache.hadoop.mapred.lib.NLineInputFormat'

extract:
	python extractMDA.py -c mrjob.conf -r emr  --emr-job-flow-id=`cat clusterid` --output-dir=s3://midsedgar/extract1/output/ --no-output s3://midsedgar/extract1/input/ 
	# python extractMDA.py -c mrjob.conf -r emr  --emr-job-flow-id=`cat clusterid` --output-dir=s3://midsedgar/extract1/output/ --no-output s3://midsedgar/extract1/input/ --hadoop-arg='-inputformat org.apache.hadoop.mapred.lib.NLineInputFormat'

clean:
	aws s3 rm s3://midsedgar/sentiment/output/ --recursive
