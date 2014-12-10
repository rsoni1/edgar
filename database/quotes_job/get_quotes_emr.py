#!/usr/bin/env python
#alex risman, MIDS 205 edgar project

#need to run "sudo pip install ystockquote" before you can import this library
import ystockquote
import urllib
import urllib2
import os
import sys
# from boto.s3.connection import S3Connection
# from boto.s3.key import Key
from datetime import date, timedelta, datetime


def main():
    # ticker_file = "input/tickers.txt"
    # bucket_name = "edgarsentimentbucket"

    # conn = S3Connection(argv[1], argv[2])
    # path_bucket = conn.get_bucket(bucket_name)
    # k = Key(path_bucket)
    # k.key = ticker_file
    # pathfile = k.get_contents_as_string()
    # try:
    #     lines = pathfile.split('\n')
    # except AttributeError:
    #     lines = pathfile

    
    try:
        print "started"
        # for linie in open(ticker_file, "r"):
        for linie in sys.stdin:
            try:
                print linie
                ticker_arr = linie.split('\t')
                curr_ticker = ticker_arr[1]
                curr_cik = ticker_arr[2]
                curr_date = ticker_arr[3]
                if not '-' in curr_date:
                    curr_date = curr_date[0:4] + '-' + curr_date[4:6] + '-' + curr_date[6:8]
                curr_date = curr_date.strip()
                curr_date_obj = crteDateObj(curr_date)
                yest_date_obj = curr_date_obj - timedelta(days=1)
                yest_date = crteDateStr(yest_date_obj)
                try:
                    price_dict = ystockquote.get_historical_prices(curr_ticker, yest_date, curr_date)
                    curr_close = price_dict[curr_date]['Close']
                    curr_adj_close = price_dict[curr_date]['Adj Close']
                    curr_open = price_dict[curr_date]['Open']
                    yest_close = price_dict[yest_date]['Close']
                    yest_adj_close = price_dict[yest_date]['Adj Close']
                    yest_open = price_dict[yest_date]['Close']
                except:
                    curr_close = "NA"
                    curr_adj_close = "NA"
                    curr_open = "NA"
                    yest_close = "NA"
                    yest_adj_close = "NA"
                    yest_open = "NA"

                try:
                    all_dict = ystockquote.get_all(curr_ticker)
                    curr_mkt_cap = all_dict['market_cap']
                except:
                    curr_mkt_cap = "NA"

                print curr_ticker + '\t' + curr_cik + '\t' + curr_date + '\t' + curr_open + '\t' + \
                 curr_close + '\t' + curr_adj_close + '\t' + yest_open + '\t' + yest_close + '\t' + \
                 yest_adj_close + '\t' + curr_mkt_cap
            except:
                print "bad"
    except:
        print "didn't start"

def crteDateObj(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    return date_obj

def crteDateStr(date_obj):
    date_str = str(date_obj)
    return date_str


if __name__ == '__main__':
    main()

