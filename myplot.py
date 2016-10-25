import pandas as pd
import datetime
import numpy

#tweets_file = open('twitter_timestamp.txt', "r")
df = pd.read_csv('twitter_timestamp.txt', names=['Timestamp'])
df[0] = pd.to_datetime(df[0], format='%m-%d-%Y %H:%M:%S')
df_2 = df.groupby(pd.TimeGrouper(freq='5Min'))
#print(df_2)


