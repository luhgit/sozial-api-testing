#!/usr/bin/env python

from flask import Flask, render_template
import facebook, requests
import simplejson as json
from collections import defaultdict

app = Flask(__name__)
app.config.from_object('config')


# Global variables
# This token will expire on October 31st, 2016
key = 'EAAZAth7DjIzwBAP1VGUTIuKG45p1yZBwPyJVFLKvGhAFUfZCP0ZCB399jPcJ5KqUtLCf82K2SyZBRZAZCE9GhdogI1WqwoD8WbZC9YLYFUZAFAiA9RIBUAgWLh13wGeEZBHXma8YPC0WIzaKZAWKRb7CLK0owUhNbWTf1kZD'
page_id = 'brexituk'
#page_id = 'rio2016'
#page_id = 'f4ep'
#page_id = 'olympics'
#page_id = 'tedxhannover'
#page_id = 'FacebookDeutschland'
content_type = 'comments,description,picture'
fb_url = ('https://graph.facebook.com/%s/posts?fields=comments' %(page_id))
postId = '921126844664117'
@app.route("/facebook")
def facebook():
	pids = ['1261709070530636']
	next = ''
	back = ''
	fb_data = fb_crawler(fb_url)
	post_comm_ids = defaultdict(list)
	for item in fb_data.items():
		if item[0] == 'data':
			for sub in item[1]:
				#if 'id' in sub:
					#if 'comments' in sub:
						for comment in sub['comments'].items():
							if comment[0] == 'data':
								for sub_com in comment[1]:
									#if ('message' or 'id' or 'created_time') in sub_com:
										post_comm_ids[sub['id'].split('_')[1]].append([sub_com['id'].split('_')[1], sub_com['message'], sub_com['created_time'], sub_com['from']['id'], sub_com['from']['name'] ])
									
		elif item[0] == 'paging':
			for sub in item[1].items():
				if sub[0] == 'next':
					next = sub[1]
				elif sub[0] == 'previous':
					back = sub[1]
	return render_template('fb_test.html', page_name = page_id, next = next, back = back, post = post_comm_ids, postId = postId, pids = pids)
	

def fb_crawler(url):
	parameters = {'fields': content_type, 'access_token': key}
	r = requests.get(url, params = parameters)
	json_data = json.loads(r.text)
	return json_data

	
@app.route("/tweet")
def tweet():
		tw_ids = [773262307942133760,481695694487145209 ,481695694487441409, 772381108017192960]
		yt_ids = ['OKcIf6UdK7c', 'rYXdsOEWBj0', 'w2tKg3E53DM', 'hTySFNbMiZo', 'hTySFNbMabcd']
		return render_template('tweet.html', TIDs = tw_ids, YIDs = yt_ids)

@app.route("/img")
def img():
		return render_template('image.html')
		
@app.route("/")
def home():
	return render_template('index.html')
if __name__ == "__main__":
	app.run(debug = True)