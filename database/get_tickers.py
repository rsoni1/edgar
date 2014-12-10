#alex risman, MIDS 205 edgar project

import sqlite3
#need to run "sudo pip install ystockquote" before you can import this library
import urllib
import urllib2
import json  
import os
import sys
from datetime import date

def main():
    ticker_file = "tickers.txt"
    try:
        os.remove(ticker_file)
    except OSError:
        pass

    ticker_file = open(ticker_file, 'w')
    conn = cnnct_db("edgarNov232014.db")
    cur = conn.cursor()
    tickers = get_tickers(cur)
    for ticker in tickers:
        try:
            curr_ticker = ticker[0]
            curr_cik = ticker[1]
            curr_date = ticker[2]
            if not '-' in curr_date:
                curr_date = curr_date[0:4] + '-' + curr_date[4:6] + '-' + curr_date[6:8]
            ticker_file.write(curr_ticker + '\t' + curr_cik + '\t' + curr_date + '\n')

        except:
            pass

    conn.close()
    ticker_file.close




def cnnct_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn


def get_tickers(cur):
    query = """
    select distinct a.ticker, a.cik, c.filingDate
    from edgar_ticker as a
    join (select ticker from
            (select ticker, count(ticker) as tck_cnt from edgar_ticker group by ticker)
            where tck_cnt = 1) as b on a.ticker = b.ticker
    join edgar_10K as c on a.cik = c.cik
    where cast(a.cik_cnt as int) < 22"""
    cur.execute(query)
    return cur.fetchall()

if __name__ == '__main__':
    main()