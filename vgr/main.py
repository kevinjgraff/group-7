#!/usr/bin/env python
#
# Copyright 2007 Google Inc.https://plus.google.com/u/0/communities/111325756615618650782?cfem=1
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import webapp2
import jinja2
import json
import os
import urllib2
import urllib
import random
from google.appengine.api import users

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))


def get_login_link(users):
	user = users.get_current_user()
	if user:
		return {'greeting': 'Welcome, %s!' % user.nickname(), 'link': users.create_logout_url('/')}
	return {'greeting': 'Sign In or Register', 'link': users.create_login_url('/')}

class MainHandler(webapp2.RequestHandler):
	def get(self):
		template = env.get_template('vgr.html')

		# self.response.out.write('<html><body>%s</body></html>' % greeting)
		self.response.out.write(template.render(get_login_link(users)))

class ResultsHandler(webapp2.RequestHandler):
	
	def get_game_list(self):
		opener = urllib2.build_opener()
		opener.addheaders = [
			('X-Mashape-Key', '5XH95HRAqnmshOFldbKVy1WQBBRZp1qTQT6jsnexDxNpTGGbnc'),
			("Accept", "application/json")
		]
		base_url = 'https://igdbcom-internet-game-database-v1.p.mashape.com/games/?'
		url_params = {'fields' : '*', 'limit' : '25','offset' : '0','order' : 'release_dates.date:desc','search' : self.request.get("query")}
		
		# base_url = 'https://igdbcom-internet-game-database-v1.p.mashape.com/genres/?'
		# url_params = {'fields' : '*', 'limit' : '10' }

		response = opener.open(base_url + urllib.urlencode(url_params))
  		return response.read()

	def get(self):
  		content_obj = json.loads(self.get_game_list())
  		template_data = {'results': content_obj}
  		template_data.update(get_login_link(users))
  # 		result_list = []
  # 		for i in style_content:
  # 			storing_dict = { "i['id']" : [ "i['name']", "i['genres']" ]  }
		# 	result_list.append( storing_dict )
		# 	# {{i['id']}} 
		# 	# {{i['name']}} 
		# 	# {{i['genres']}} 
		# print result_list

		#style_content = {'style_key': names}
		template = env.get_template('results.html')

		self.response.write(template.render(template_data))

class RecHandler(webapp2.RequestHandler):
	def get(self):
  		# style_content.update(get_login_link(users)
		template = env.get_template('info.html')
		# game_id = self.request.get('id')
		# game_name = self.request.get('name')
		# game_story = self.request.get('summary')
		# data = {'id': game_id, 'name' :game_name, 'summary': game_story}
  		# data.update(get_login_link(users))

  		opener = urllib2.build_opener()
		opener.addheaders = [
			('X-Mashape-Key', '5XH95HRAqnmshOFldbKVy1WQBBRZp1qTQT6jsnexDxNpTGGbnc'),
			("Accept", "application/json")
		]
		def game_info_from_id(game_id):
			game_url = 'https://igdbcom-internet-game-database-v1.p.mashape.com/games/' + game_id + '?'
			game_url_params = {'fields' : '*'}
			game_response = opener.open(game_url + urllib.urlencode(game_url_params)).read()
	  		game_content_obj = json.loads(game_response)

	  		return game_content_obj

		
		game_content_obj = game_info_from_id(self.request.get('id'))
		genre = game_content_obj[0]['genres'][0]

		print "Genre is"
		print genre

		genre_url = 'https://igdbcom-internet-game-database-v1.p.mashape.com/genres/' + str(genre) + '?'
		genre_url_params = {'fields' : '*', 'limit' : '10' }
		genre_response = opener.open(genre_url + urllib.urlencode(genre_url_params)).read()
		genre_content_obj = json.loads(genre_response)

  		

  		# len_of_genre_games = len(genre_content_obj[0]['games'])
  		# rand_genre_games = random.sample(genre_content_obj[0]['games'], 20)

  		# print len_of_genre_games
  		# print rand_genre_games


  		rec_id_list = rand_genre_games = random.sample(genre_content_obj[0]['games'], 20)
  		rec_list = []

  		for rec in rec_id_list:
  			rec_list.append(game_info_from_id(str(rec)))
  
		template_data = {
			'game_info': game_content_obj,
			'genre_info': genre_content_obj,
			'rec_info' : rec_list
		}
		self.response.write(template.render(template_data))

class NewsHandler(webapp2.RequestHandler):
	def get(self):
		template = env.get_template('news.html')
		self.response.write(template.render(get_login_link(users)))

class ContactHandler(webapp2.RequestHandler):
	def get(self):
		template = env.get_template('contact.html')
		self.response.write(template.render(get_login_link(users)))

class AboutHandler(webapp2.RequestHandler):
	def get(self):
		template = env.get_template('about.html')
		self.response.write(template.render(get_login_link(users)))


app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/news', NewsHandler),
	('/contact', ContactHandler),
	('/about', AboutHandler),
	('/results', ResultsHandler),
	('/info', RecHandler)

], debug=True)
