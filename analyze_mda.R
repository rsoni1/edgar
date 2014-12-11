# MIDS 205 Final Project R Script

library(RSQLite)
library(ggplot2)
library(stringr)

# Function: used to trim leading and trailing whitespace
trim <- function (x) gsub("^\\s+|\\s+$", "", x)

# Create connection to the DB
drv <- dbDriver("SQLite")
con <- dbConnect(drv, "edgar_sentiment.db")

# make sure DB looks right, just print out the tables and fields for the sentiment table
dbListTables(con)
dbListFields(con, "sentiment_two")

# put data fron the DB into a dataframe
sentimentdata = dbGetQuery(con, "SELECT polarity, positive, negative, subjectivity, filing_url FROM sentiment_two")

# add a new column that sums up the number of total ranked words and then the % positive
sentimentdata$rankedwords = sentimentdata$positive + sentimentdata$negative
sentimentdata$perc_positive = sentimentdata$positive / sentimentdata$rankedwords

# examine the summary statistics
summary(sentimentdata)

# first, lets look at what the distribution of polarity is
polarityPlot = ggplot(sentimentdata, aes(polarity))
polarityPlot + geom_histogram(binwidth=.01)
# ... looks like there is a set of polarities that are simply 1.  also there are some negative polarities.  think abour removing from analysis

# also, lets look at what the distributions the percent positive is
perPosPlot = ggplot(sentimentdata, aes(perc_positive))
perPosPlot + geom_histogram(binwidth=.01)
# ... again, looks like there are simply 100% positive MDAs. think about removing from analysis

# put data fron the DB into a dataframe for CIKs and paths
cikdata = dbGetQuery(con, "SELECT * FROM edgar_10K")

# trim the cik data and order it for easier debugging
cikdata$filingURL = trim(cikdata$filingURL)
order.cik <- order(cikdata$cik, cikdata$filingDate)
cikdata = cikdata[order.cik,]

# get the quote data in a dataframe
quotedata = dbGetQuery(con, "SELECT * FROM quotes")
order.cik <- order(quotedata$CIK, quotedata$date)
quotedata = quotedata[order.cik,]

# join the sentiment data and cik data.
joineddata  = merge(sentimentdata, cikdata, by.x="filing_url", by.y="filingURL")

# join the sentiment/cik data with the price quote date
finaljoineddata = merge(joineddata, quotedata, by.x = c("cik","filingDate"), by.y=c("CIK","date"))

# run some data on what how many rows of data we are ending up with for the analysis
cikrows = sum(complete.cases(cikdata))
quotesrows = sum(complete.cases(quotedata))
sentimentrows = sum(complete.cases(sentimentdata))
finaljoinedrows = sum(complete.cases(finaljoineddata))
roundPercFinal = round(finaljoinedrows / sentimentrows,3)*100

cat("Sentiment data contains:", sentimentrows, "rows\nQuotes data contains:", quotesrows,"rows\nFinal joined data contains:", finaljoinedrows,"rows\n", "The final % of Section 7 MD&A with sentiment data included in the analysis is:", roundPercFinal,"%")

# look at the perc positive plot in the final dataframe
perPosPlot = ggplot(finaljoineddata, aes(perc_positive))
perPosPlot + geom_histogram(binwidth=.01)
# ... it doesn't look too different in structure relative to the pre joined version

# look at the summary statistics of the final dataframe
summary(finaljoineddata)
# ... af few items stick out.  first, in ranked words, the max is much higher than the average which looks like a/some outlier(s).  Also, there appear to be some open and close prices that are not right (0 and 1000000).  lets remove those from the analysis

index.examineoutliers = finaljoineddata$open_price > 10000
outliersdata = finaljoineddata[index.examineoutliers,]
# ... this yields some data, some of which looks legitimate (Berkshire Hathaway) and some which looks incorrect with a price of 10000000.  

# lets remove those high price outliers
index.valid = finaljoineddata$open_price != 10000000
finaljoineddata = finaljoineddata[index.valid,]

# now lets examine the price outliers on the bottom of the scale
index.examineoutliers = finaljoineddata$open_price < .01
outliersdata = finaljoineddata[index.examineoutliers,]
# ... this yields some data as well, there are about 200 observations that are at 0 or close to 0.  These won't be particularly useful to our analysis, so we remove them as well.  in addition, looking at the behaviour of stocks below $1, there are quite a few anomolous days with 0 change in price.  

# remove price outliers on the lower end
index.valid = finaljoineddata$open_price >= 1
finaljoineddata = finaljoineddata[index.valid,]

# another look at the summary
summary(finaljoineddata)

# now create a feature for the differnce in prices in $ terms and % terms
finaljoineddata$pricediff = finaljoineddata$close_price - finaljoineddata$open_price
finaljoineddata$pricediffperc = finaljoineddata$pricediff / finaljoineddata$open_price

finaljoineddata$sent_revised = log((1+finaljoineddata$positive)/(1+finaljoineddata$negative))
finaljoineddata$price_up = ifelse(finaljoineddata$pricediff<0,0,1)
finaljoineddata$sent_pos = ifelse(finaljoineddata$positive>finaljoineddata$negative,1,0)

# lets examine the pricing data to ensure that it looks correct
priceplot = ggplot(finaljoineddata, aes(pricediffperc))
priceplot + geom_histogram(binwidth=.01)
# ... it looks like we could still remove some outliers since so much of the data is clusterd around zero, lets keep all the data for now

sentModel1 = lm(pricediffperc ~ perc_positive, data=finaljoineddata)
summary(sentModel1)

sentModel2 = lm(price_up ~ sent_pos, data=finaljoineddata)
summary(sentModel2)

# TO DO STILL: 1) remove outlier sentiment values on the high end and low end and at 0; 2) remove the low end ending prices ;3) use adjusted prices and perhaps day before prices






