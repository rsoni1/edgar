#alex risman, MIDS 205 edgar project

#need to run "sudo pip install ystockquote" before you can import this library
import ystockquote
import urllib
import urllib2
import os
import sys
#from datetime import date

def main():
    error_file = "no_quote.txt"
    ticker_file = "tickers.txt"
    quotes_file = "quotes.txt"

    error_file = open(error_file, 'w')
    ticker_file = open(ticker_file, 'r')
    quotes_file = open(quotes_file, 'w')

    for ticker in ticker_file:
        try:
            ticker_arr = ticker.split('\t')
            curr_ticker = ticker_arr[0]
            curr_cik = ticker_arr[1]
            curr_date = ticker_arr[2]
            if not '-' in curr_date:
                curr_date = curr_date[0:4] + '-' + curr_date[4:6] + '-' + curr_date[6:8]
            # crteDateObj(curr_date)
            price_dict = ystockquote.get_historical_prices(curr_ticker, curr_date, curr_date)
            if curr_date in price_dict and 'Close' in price_dict[curr_date] and 'Open' in price_dict[curr_date]:
                curr_close = price_dict[curr_date]['Close']
                curr_open = price_dict[curr_date]['Open']
                quotes_file.write(curr_ticker + '\t' + curr_cik + '\t' + curr_date + '\t' + curr_open + '\t' + curr_close)

        except:
            error_file.write(curr_ticker + ', ' + curr_cik + ', ' + curr_date) 

    error_file.close()
    ticker_file.close()
    quotes_file.close()

def crteDateObj(date_str):
    date_arr = date_str.split("-")
    curr_year = date_arr[0]
    curr_mnth = date_arr[1]
    curr_day = date_arr[2]
    date_obj = date(curr_year, curr_mnth, curr_day)
    return date_obj

if __name__ == '__main__':
    main()

