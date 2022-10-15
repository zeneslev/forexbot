#!/usr/bin/env python


from datetime import datetime
import pandas as pd
import csv 
import plotly.graph_objects as go


# making dataframe 
df = pd.read_csv("USD_JPY_M5.csv", parse_dates=["Time"]) #Set the time column to be datetime objects
   
# output the dataframe
#print(df)

#print(df.info(verbose=True)) #Tells us what type of objects are in the dataframe

#print (df.iloc[0]) #Print index 0

df.set_index('Time', inplace=True)#Make datafram indexable by datetime

print(df.loc['2022-10-07 02:00:00'])

print(df.loc['Oct 05, 2022 5:00pm']) #Indexing like this is also possible. Wow!


df_no_parse = pd.read_csv("USD_JPY_M5.csv") #Set the time column to be datetime objects

fig = go.Figure(data=[go.Candlestick(x=df_no_parse['Time'],
                open=df_no_parse['Open'],
                high=df_no_parse['High'],
                low=df_no_parse['Low'],
                close=df_no_parse['Close'])])

fig.show()