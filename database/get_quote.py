#alex risman, MIDS 205 edgar project

import sqlite3
#need to run "sudo pip install ystockquote" before you can import this library
import ystockquote
import urllib
import urllib2
import json  
import os

def main():
    error_file = "no_quote.txt"
    try:
        os.remove(error_file)
    except OSError:
        pass

    error_file = open(error_file, 'w')
    conn = cnnct_db("edgarNov232014.db")
    cur = conn.cursor()
    cur = create_table(cur, "quotes", " (ticker text, CIK int, date text, open_price real, close_price real)")
    tickers = get_tickers(cur)
    for ticker in tickers:
        try:
            curr_ticker = ticker[0]
            curr_cik = ticker[1]
            curr_date = ticker[2]
            if not '-' in curr_date:
                curr_date = curr_date[0:4] + '-' + curr_date[4:6] + '-' + curr_date[6:8]
            price_json = ystockquote.get_historical_prices(curr_ticker, curr_date, curr_date)
            if curr_date in price_json and 'Close' in price_json[curr_date] and 'Open' in price_json[curr_date]:
                curr_close = price_json[curr_date]['Close']
                curr_open = price_json[curr_date]['Open']
                data = [curr_ticker, curr_cik, curr_date, curr_open, curr_close]
                print data
                cur = insert_data(cur, "quotes", data)

        except:
            error_file.write(curr_ticker + ', ' + curr_cik + ', ' + curr_date) 

    conn.commit()
    conn.close()
    error_file.close




def cnnct_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn

def create_table(cur, tname, col_string):
    query = 'create table if not exists ' + tname + col_string
    cur.execute(query)
    return cur

def clear_table(cur, tname):
	query = 'delete from ' + tname
	cur.execute
	return cur

def insert_data(cur, tname, data):
    query = 'insert into ' + tname + ' values ("' + str(data[0]).strip() + '", "' + str(data[1]).strip() + '", "' + str(data[2]).strip() + '", "' + str(data[3]).strip() + '", "' + str(data[4]).strip() + '")'
    cur.execute(query)
    return cur

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

