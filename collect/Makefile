clean:
	aws s3 rm s3://midsedgar/extract/ --recursive
extract:
	head -5 master.idx | python extractMDA.py
