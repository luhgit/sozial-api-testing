#!/usr/bin/env python

from flask import Flask, render_template, request, jsonify
import facebook, requests
import json
from collections import defaultdict
import vincent

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
pids_full = ['1102184159816462_1261709070530636']
content_type = 'comments'
fb_url = ('https://graph.facebook.com/%s' %(pids_full[0]))

@app.route("/facebook")
def facebook():
	test_list = defaultdict(list)
	next = ''
	back = ''
	fb_data = fb_crawler(fb_url)
	post_comm_ids = defaultdict(list)
	for item in fb_data.items():
		if type(item[1]) == dict:
			for sub in item[1]['data']:
				for sub in sub.items():
					if sub[0] == 'id':
						test_list[sub[1].split('_')[0]].append(sub[1].split('_')[1])

	return render_template('fb.html', page_name_or_id = pids_full[0].split('_')[0], postId = [pids_full[0].split('_')[1]], test = fb_data, tlist = test_list)
	
@app.route("/posts")
def fb_posts():
	posts = ['1261709070530636', '1270577636310446', '1267802689921274', '10154273475361281']
	return jsonify(res = posts)

@app.route("/comments")
def fb_comment():
	fb_data = fb_crawler(fb_url)
	post_comm_ids = defaultdict(list)
	#test_list = ['123', ['456', '789'],]
	for item in fb_data.items():
		if type(item[1]) == dict:
			for sub in item[1]['data']:
				for sub in sub.items():
					if sub[0] == 'id':
						post_comm_ids[sub[1].split('_')[0]].append(sub[1].split('_')[1])
	return jsonify(res = post_comm_ids)

@app.route('/ajax')
def index():
    return render_template('ajax.html')

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


def fb_crawler(url):
	parameters = {'fields': content_type, 'access_token': key}
	print(url)
	r = requests.get(url, params = parameters)
	print(r.text)
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

# Testing modeules

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username'];
    password = request.form['password'];
    return json.dumps({'status':'OK','user':user,'pass':password});

@app.route('/relevance')
def relevance():
    return render_template('relevance.html')

@app.route('/hashtags')
def rel_data():
	hashtags = ['#donald', '#clinton', '#uselection', '#election2016', '#uselection2016', '#gop', '#democrats', '#rebublicans', '#preseidentialdebate', '#debate', '#whitehouse']
	return jsonify(res = hashtags)

@app.route('/judgement', methods=['POST'])
def judgement():
	if request.method == 'POST':
		judgements =  request.data
		print(judgements.decode())
		f = open('form_data.txt','w')
		f.write(judgements.decode())
		f.close()
	return render_template('relevance.html')

@app.route("/")
def home():
	return render_template('index.html')

@app.route("/test")
def test():
	return render_template('test.html')

@app.route("/ids")
def IDs():
	ids = ['1102184159816462_1261709070530636']
	#ids = ['1102184159816462_1261709070530636', '1102184159816462_1270577636310446', '1102184159816462_1267802689921274', '1102184159816462_10154273475361281']
	return jsonify(res = ids)

@app.route("/token")
def token():
	token = "EAACEdEose0cBAGN0gtZCLrehJPlaJye4m8LrMQQF2LLc4KAf246vX4KhmECVqJgRUq8zKv42YdZCOihhGIzUIYGB85oq1dj8ZCndxNVnc4Nn46xoY91A4JYA7a7p7gQvbRI6DATS52N8zXvtMZA7VbN7qp4NtXHa0WqVPlzTmAZDZD";
	return jsonify(res = token)


if __name__ == "__main__":
	app.run(debug = True)
	fb_crawler(fb_url)