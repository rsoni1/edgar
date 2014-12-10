#alex risman, MIDS 205 edgar project

import sqlite3
#need to run "sudo pip install ystockquote" before you can import this library
import ystockquote
import urllib
import urllib2
import json  
import os
import sys
from datetime import date

def main():
    r_sent_file = "r_sent_tbl.txt"
    try:
        os.remove(r_sent_file)
    except OSError:
        pass

    r_sent_file = open(r_sent_file, 'w')
    conn = cnnct_db("edgar_sentiment.db")
    cur = conn.cursor()
    sent_stuff = get_sent_stuff(cur)
    r_sent_file.write("ticker" + '\t' + "cik" + '\t' + "date" + '\t' + "open_price" + '\t' + "close_price" + '\t' + "polarity" + '\t' + "positive" + '\t' + "negative" + '\t' + "subjectivity" + '\n')
    for sentie in sent_stuff:
        print sentie
        curr_ticker = sentie[0]
        curr_cik = sentie[1]
        curr_date = sentie[2]
        curr_open = sentie[3]
        curr_close = sentie[4]
        curr_pol = sentie[5]
        curr_pos = sentie[6]
        curr_neg = sentie[7]
        curr_subj = sentie[8]
        r_sent_file.write(curr_ticker + '\t' + curr_cik + '\t' + curr_date + '\t' + curr_open + '\t' + curr_close + '\t' + curr_pol + '\t' + curr_pos + '\t' + curr_neg + '\t' + curr_subj + '\n')
    conn.close()
    r_sent_file.close()




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

def get_sent_stuff(cur):
    # query = """
    # select distinct a.ticker, a.cik, a.date, a.open_price, a.close_price, c.polarity, c.positive, c.negative, c.subjectivity
    # from quotes a
    # join edgar_10K b on a.date = b.filingDate and a.cik = b.cik
    # join sentiment c on b.filingURL = c.filing_url"""
    query = """
    select distinct a.cik
    from edgar_10K a
    join sentiment b on a.filingURL = b.filing_url"""
    cur.execute(query)
    return cur.fetchall()

if __name__ == '__main__':
    main()

