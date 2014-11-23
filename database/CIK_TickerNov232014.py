import sqlite3
import re
import urllib
import urllib2
import json  
from time import time, sleep                  
                                  
                                                  
 # http://www.cornerofberkshireandfairfax.ca/forum/general-discussion/sec-edgar-gurus-%28and-financial-programmers%29/
def cik_ticker(cik):
    #print "Searching for symbol that matches %s" % cik
    yahoo_url = 'http://finance.yahoo.com/lookup?s='
    edgar_url = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK=%s&action=getcompany' % cik
    string_match = 'companyName'
    # Fetch company page from edgar using the CIK
    response = urllib2.urlopen(edgar_url)
    edgar_company_name = 'No Edgar Name'
    for line in response:
        if string_match in line:
           name_match = re.search('<span class="companyName">(.*)<acronym', line)
           company_name = name_match.group(1)
           company_name = company_name.replace('&amp;', '&')
           #print "Found company name %s from SEC" % company_name
           edgar_company_name = company_name

    # Here we do some fuzzy logic. If the company name has more than 
    # three words then only use the first two unless the second word
    # is 2 chars or less.
    #if len(company_name.split()) >= 2:
    #    company_name_words = company_name.split()
    #    #print company_name_words, len(company_name_words)
    #    if len(company_name_words[1]) <= 2 and len(company_name_words) >= 3:
    #        company_name = '%s %s %s' % (company_name_words[0],
    #                                 company_name_words[1],
    #                                 company_name_words[2])
    #    else:
    #        company_name = '%s %s' % (company_name_words[0], company_name_words[1])
    if len(company_name.split()) >= 3:
        company_name_words = company_name.split()
        #print company_name_words, len(company_name_words)
        if len(company_name_words[2]) <= 2 and len(company_name_words) >= 4:
            company_name = '%s %s %s %s' % (company_name_words[0],
                                     company_name_words[1],
                                     company_name_words[2],
                                     company_name_words[3])
        else:
            company_name = '%s %s %s' % (company_name_words[0], company_name_words[1], company_name_words[2])        

    #print "Attempting to search yahoo finance for %s" % company_name
    # URL encode the company name
    company_name = urllib.quote(company_name)

    #Take the company name to yahoo and get the ticker
    # yahoo_url = 'http://finance.yahoo.com/lookup?s=%s' % company_name
    # yahoo_url = 'http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=yahoo&callback=YAHOO.Finance.SymbolSuggest.ssCallback'
    # http://stackoverflow.com/questions/885456/stock-ticker-symbol-lookup-api
    yahoo_url = 'http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=%s&callback=YAHOO.Finance.SymbolSuggest.ssCallback' % company_name
    #print "Yahoo search URL is %s" % yahoo_url
    response = urllib2.urlopen(yahoo_url)
    lines = response.read()
    #print lines
    json_string = json.dumps(lines)
    j = json.loads(json_string) # j has type string   
    # {"symbol":"SDA","name": "Bank of America Corporation Mar","exch": "PCX","type": "S","exchDisp":"NYSEArca","typeDisp":"Equity"}
    #print j
    names=[edgar_company_name]
    for item in j.split("{"):
        item1 = item.translate({ord(i):None for i in '}])'})
        if ('"exchDisp":"NASDAQ"' in item1 or '"exchDisp":"OTC Markets"' in item1 or '"exchDisp":"NYSE"' in item1 or '"exchDisp":"AMEX"' in item1 or '"exchDisp":"NYSEArca"' in item1) and '"typeDisp":"Equity"' in item1: #US Exchanges: 
            item2 = item1.replace('"symbol":','')
            item3 = item2.replace('"name":','')
            item4 = item3.replace('"exch":','')
            item5 = item4.replace('"type":','')
            item6 = item5.replace('"exchDisp":','')
            item7 = item6.replace('"typeDisp":','')
            allitems = item7.split('"')
            if len(allitems) == 13:
                names.append(str(allitems[1]))
                names.append(str(allitems[3]))
                names.append(str(allitems[9]))
    return names                
                                                                                                                                                                                                                                                                                                       
conn = sqlite3.connect('edgar.db')
conn.text_factory = str
cur = conn.cursor()    
sql = """
SELECT cik, count(*) as cnt 
FROM edgar_index 
WHERE filingType = '10-K' 
GROUP BY cik 
HAVING cnt = 1
ORDER BY cnt DESC
"""
cur.execute(sql)
CIKs = cur.fetchall()
print CIKs
#cur.execute("DROP TABLE IF EXISTS edgar_ticker")
#cur.execute('''CREATE TABLE edgar_ticker (cik, cik_cnt, c_name, y_name, ticker, exch)''') 
cik_cnt = 1
for CIK in CIKs:    
    #print str(CIK[0]), str(CIK[1]) 
    res = cik_ticker(str(CIK[0]))
    datacnt = 1
    c_name=' '
    ticker = ' '
    y_name = ' '
    exch = ' '
    for i in res:
        #print i
        if datacnt == 1:
            c_name = i
        if datacnt == 2:
            y_name = i    
        if datacnt == 3:
            ticker = i    
        if datacnt == 4:
            exch = i         
        datacnt +=1               
    print cik_cnt, str(CIK[0]), str(CIK[1]), c_name, ticker, y_name, exch  
    cur.execute("""INSERT INTO edgar_ticker(cik, cik_cnt, c_name, y_name, ticker, exch) 
                          VALUES (?,?,?,?,?,?);""", (str(CIK[0]), str(CIK[1]), c_name, ticker, y_name, exch))    
    cik_cnt += 1
    sleep(3)
    conn.commit()
    #if cik_cnt > 100:
    #    break 
conn.commit()                                       
conn.close()

