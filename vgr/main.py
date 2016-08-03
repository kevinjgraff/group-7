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
#

import webapp2
import jinja2
import json
import os
import urllib2
import urllib
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
		url_params = {'fields' : 'name', 'limit' : '20','offset' : '0','order' : 'release_dates.date:desc','search' : self.request.get("query")}
		#response = opener.open('https://igdbcom-internet-game-database-v1.p.mashape.com/games/?')
		response = opener.open(base_url + urllib.urlencode(url_params))
		 # response = unirest.get("https://igdbcom-internet-game-database-v1.p.mashape.com/genres/?fields=*&limit=40",
 		# headers ={  "X-Mashape-Key": "5XH95HRAqnmshOFldbKVy1WQBBRZp1qTQT6jsnexDxNpTGGbnc"}  )
  		return response.read()

	def get(self):
  		content_obj = json.loads(self.get_game_list())
  		style_content = {'style_key': content_obj}
  		style_content.update(get_login_link(users))

		#style_content = {'style_key': names}
		template = env.get_template('results.html')

		self.response.write(template.render(style_content))

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
	('/results', ResultsHandler)
], debug=True)
