# Murat Aydogdu
# EDGAR indices (daily for the current quarter, quarterly for all quarters preceding this one)

# Company name (eg. ```TWITTER, INC```)
#  - Company CIK (eg.``` 0001418091```)
#  - Filling date (eg. ```2013-10-03```)
#  - Filling type (eg. ```S1```)
#  - Filling URL on EDGAR (```edgar/data/1418091/0001193125-13-390321.txt```)

import edgar
import ftplib
import os
import sqlite3
from os import listdir
from os.path import isfile, join


#ftp = ftplib.FTP(edgar.FTP_ADDR)
#ftp.login()
#try:
#    edgar.download_all(ftp, "/Users/murataydogdu/Google Drive/UCB_MIDS_StartingSummer2014/2014_Fall/W205_SaRD/edgar/tmp")
#except Exception as e:
#    print e
#finally:
#    ftp.close()
            
mypath='/Users/murataydogdu/Google Drive/UCB_MIDS_StartingSummer2014/2014_Fall/W205_SaRD/edgar/tmp/'
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
print onlyfiles

conn = sqlite3.connect('edgar.db')
conn.text_factory = str
cur = conn.cursor()
cur.execute('''CREATE TABLE edgar_index (cik, c_name, filingType, filingDate, filingURL)''') 
cn = 1
for f in onlyfiles:
    print f
    with open(f, 'r') as fp:
        for line in fp:
            data = line.split('|')
            cnt = 1
            cik = ' '
            c_name = ' '
            filingType = ' '
            filingDate = ' ' 
            filingURL = ' '
            for i in data:
                #print i, cnt
                if cnt == 1:
                    cik = i
                if cnt == 2:
                    c_name = i
                if cnt == 3:
                    filingType = i  
                if cnt == 4:
                    filingDate = i 
                if cnt == 5:
                    filingURL = i
                cnt +=1               
                #print cik, c_name, filingType, filingDate, filingURL        
                #cur = insert_data(cur, table, cik, c_name, filingType, filingDate, filingURL)
            cur.execute("""INSERT INTO edgar_index(cik, c_name, filingType, filingDate, filingURL) 
                              VALUES (?,?,?,?,?);""", (cik, c_name, filingType, filingDate, filingURL))    
            #cn += 1
            #if cn > 100: 
            #    break        
                                      
conn.commit()
conn.close()


