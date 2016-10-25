import json
from datetime import timedelta
import pandas as pd
import numpy as np
import math
import datetime, time, arrow
import matplotlib.pyplot as plt


def drawPlot(x, y):
	# t = linspace(0,2*math.pi,400)
	# a = sin(t)
	# b = cos(t)
	# c = a + b

	# plt.plot(t,a,'r') # plotting t,a separately 
	# plt.plot(t,b,'b') # plotting t,b separately 
	# plt.plot(t,c,'g') # plotting t,c separately 
	# plt.show()
	x = np.linspace(x[0], x[len(x) -1])
	y = np.linspace(y[0], y[len(x) -1])    
	plt.show(x,y)
# To group the timestamps in the defined period for count(tweet_ids)
def group_timestamps(timestamps):
	current = timestamps[0]
	count = 0
	grouped = []
	for t in timestamps:
		if (t - current) <=  timedelta(minutes=1):
			count = count + 1
		else:
			grouped.append([str(current), count])
			current = t
			count = 1
	grouped.append([str(current), count])
	stamps = []
	counts = []
	for i in grouped:
		print(i[0] + ", " + str(i[1]+50))
		stamps.append(i[0])
		counts.append(i[1])
	#drawPlot(stamps, counts)

def gen_timestamp(val):
	unix_timestamp = time.mktime(time.strptime(val,"%a %b %d %H:%M:%S %z %Y"))
	return datetime.datetime.fromtimestamp(unix_timestamp)
	#return arrow.Arrow.strptime(val, "%a %b %d %H:%M:%S %z %Y")
def unpack(LIST):
	hashtags = []
	for tag in LIST:
		hashtags.append(tag['text'])
	return hashtags

def count_hashtags_or_tweets():
	tweets_data_path = 'test_debate.txt'
	timestamps = []
	tweets_file = open(tweets_data_path, "r")
	for line in tweets_file:
		try:
			tweet = json.loads(line)
			#if (len(tweet['entities']['hashtags']) == 0):
			#	continue
			# Counts all the Hashtags in the dataset
			#print(str(tweet['id']) + ',  ' + str(unpack(tweet['entities']['hashtags'])))
			#for i in tweet['entities']['hashtags']:
			#	print(i['text'])
			#print('\n'.join('{}'.format(k) for k in enumerate(tweet['entities']['hashtags'])))
			# Counts all the Timestamps
			timestamp = gen_timestamp(tweet["created_at"])
			print(timestamp)
			timestamps.append(timestamp)
		except:
			continue
	print(len(timestamps))
	#group_timestamps(timestamps)


def count_unique_tweets():
	tweets_data_path = 'twitter_debate.txt'
	timestamps = []
	tweets_file = open(tweets_data_path, "r")
	for line in tweets_file:
		try:
			tweet = json.loads(line)
			print(str(tweet['text']))

		except:
			continue

count_hashtags_or_tweets()
#count_unique_tweets()
#drawPlot()