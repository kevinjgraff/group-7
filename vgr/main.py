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

class MainHandler(webapp2.RequestHandler):
	def get(self):
		template = env.get_template('vgr.html')
		user = users.get_current_user()
		if user:
			greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
				(user.nickname(), users.create_logout_url('/')))
		else:
			greeting = ('<a href="%s"> Sign in or register</a>' %
				users.create_login_url('/'))

		user_data = {'user':greeting}
		# self.response.out.write('<html><body>%s</body></html>' % greeting)
		self.response.out.write(template.render(user_data))

class ResultsHandler(webapp2.RequestHandler):
	def get(self):

		'''base_url = 'https://en.wikipedia.org/w/api.php?'
		url_params = {'titles': self.request.get('query'), 'action': 'query', 'prop' : 'revisions', 'rvprop' : 'content' , 'format' : 'json'}
		#response = urllib2.urlopen("https://en.wikipedia.org/w/api.php? action=query &titles=Main%20Page &prop=revisions &rvprop=content &format=json")
		resource = base_url + urllib.urlencode(url_params)
		#print resource
		response = urllib2.urlopen(resource)
		content = response.read()
		#print content
		content_obj = json.loads(content)
		variable_id = 0
		for pages in content_obj['query']['pages']:
			variable_id = pages
			break 
		#for key in content_obj['query']['pages']['variable_id']['revisions'][0]['*']:
		#	game_page = key
		print variable_id
		wiki_begin_page = content_obj['query']['pages'][variable_id]['revisions'][0]['*']
		print 'test'
		print wiki_begin_page
		genreIndex = wiki_begin_page.find("genre")
		print wiki_begin_page[genreIndex:genreIndex+100]
		genreUnformatted = wiki_begin_page[genreIndex : genreIndex + 200]
		genre = genreUnformatted[ (genreUnformatted.find("|")+1) : genreUnformatted.find("]")]
		print genre'''

		opener = urllib2.build_opener()
		opener.addheaders = [
			('X-Mashape-Key', '5XH95HRAqnmshOFldbKVy1WQBBRZp1qTQT6jsnexDxNpTGGbnc'),
			("Accept", "application/json")
		]
		base_url = 'https://igdbcom-internet-game-database-v1.p.mashape.com/games/?'
		url_params = {'fields' : 'name', 'limit' : '20','offset' : '0','order' : 'release_dates.date:desc','search' : self.request.get("query")}
		#response = opener.open('https://igdbcom-internet-game-database-v1.p.mashape.com/games/?')
		response =opener.open( base_url + urllib.urlencode(url_params))
		print response
		 # response = unirest.get("https://igdbcom-internet-game-database-v1.p.mashape.com/genres/?fields=*&limit=40",
 		# headers ={  "X-Mashape-Key": "5XH95HRAqnmshOFldbKVy1WQBBRZp1qTQT6jsnexDxNpTGGbnc"}  )
  		content = response.read()
  		print ""
  		print ""
  		print "The content is"
  		print content


  		content_obj = json.loads(content)
  		style_content = {'style_key': content_obj}

		#style_content = {'style_key': names}
		template = env.get_template('results.html')

		self.response.write(template.render(style_content))

class NewsHandler(webapp2.RequestHandler):
	def get(self):
		template = env.get_template('news.html')
		self.response.write(template.render())

class ContactHandler(webapp2.RequestHandler):
	def get(self):
		template = env.get_template('contact.html')
		self.response.write(template.render())

class AboutHandler(webapp2.RequestHandler):
	def get(self):
		template = env.get_template('about.html')
		self.response.write(template.render())


app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/news', NewsHandler),
	('/contact', ContactHandler),
	('/about', AboutHandler),
	('/results', ResultsHandler)
], debug=True)
