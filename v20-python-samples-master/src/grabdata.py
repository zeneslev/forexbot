#!/usr/bin/env python

import argparse
import common.args
from instrument.view import CandlePrinter
from order.view import print_order_create_response_transactions
import v20
from datetime import datetime
import pytz
import pandas as pd

import csv 


api = v20.Context(
        hostname="api-fxtrade.oanda.com",
        token="e399afd64c7048d997d83b29f3a5efbd-78cef64066e78f15829afb5a9fe0bfe4"
)

#response = api.account.get('001-001-7995786-001')

#print("Response: {} ({})".format(response.status, response.reason))


kwargs = {}

#if args.granularity is not None:
kwargs["granularity"] = "M5"
kwargs["count"] = 5000

response = api.instrument.candles("USD_JPY", **kwargs)

if response.status != 200:
        print(response)
        print(response.body)

#print("Instrument: {}".format(response.get("instrument", 200)))
#print("Granularity: {}".format(response.get("granularity", 200)))

printer = CandlePrinter()





#Convert to EST?

#print (type(response))
#print (response.body) #This has all the data
#print (response.raw_body) #This too!
#print (response.lines)

gmt_tz = pytz.timezone('GMT')
my_tz = pytz.timezone('America/New_York')

for candle in response.get("candles", 200):
        dt = datetime.strptime(candle.time,"%Y-%m-%dT%H:%M:%S.000000000Z")
        aware_dt = gmt_tz.localize(dt)

        new_tz_time = aware_dt.astimezone(my_tz)

        naive_dt = new_tz_time.replace(tzinfo=None)
        #print(str(naive_dt))

        candle.time = str(naive_dt)

        #print(candle.time)


#printer.print_header()
#for candle in response.get("candles", 200):
#        printer.print_candle(candle)


#Make giant CSV
# name of csv file 
filename = "USD_JPY_M5.csv"
# writing to csv file 
with open(filename, 'w',newline='\n') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 

        # field names 
        fields = ['DateTime', 'Open', 'High', 'Low', 'Close','Volume']        
        # writing the fields 
        csvwriter.writerow(fields) 

        for candle in response.get("candles", 200):
                dt = candle.time
                volume = candle.volume
                open = getattr(candle, 'mid', None).o
                high = getattr(candle, 'mid', None).h
                low = getattr(candle, 'mid', None).l
                close = getattr(candle, 'mid', None).c
                csvwriter.writerow((dt,open,high,low,close,volume))
        








    

    


#df = pd.DataFrame()
#print (df)