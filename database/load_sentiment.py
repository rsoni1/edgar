#alex risman, MIDS 205 edgar project

import sqlite3
import urllib
import urllib2
import json  
import os
import sys
from itertools import islice 

def main():
    #sent_file = "sentiment_data_2_Loughran.txt"
    sent_file = "awsoutput.txt"
    sent_file = open(sent_file, 'r')
    sent_table = "sentiment"
    conn = cnnct_db("edgar_sentiment.db")
    cur = conn.cursor()
    cur = create_table(cur, sent_table, " (filing_url text, polarity real, positive real, negative real, subjectivity real)")
    cur = clear_table(cur, sent_table)
    for line in sent_file:
        arr = line.split('.txt\',')
        filing_url = arr[0] + '.txt'
        sent_dict = arr[1]
        filing_url = filing_url.replace("(\'", "").replace("extract", "edgar/data")
        sent_dict = sent_dict.replace("\"", "").replace(")", "").replace("{", "").replace("}", "").replace("\t\n", "").split(", ")
        sent_parms = []
        for sent in sent_dict:
            sent = sent.split(": ")
            sent_parms.append(sent)
        curr_pol = sent_parms[0][1]
        curr_pos = sent_parms[1][1]
        curr_neg = sent_parms[2][1]
        curr_subj = sent_parms[3][1]
        data = [filing_url, curr_pol, curr_pos, curr_neg, curr_subj]
        print(data)
        cur = insert_data(cur, sent_table, data)
        conn.commit()
    conn.close()
    sent_file.close()




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

if __name__ == '__main__':
    main()

