#!/usr/bin/env python

""" 
Flickr Downloader

Downloads all your images into a directory called "backup". Doesn't have error handling, much.

Uses code from Dr. Drang (http://leancrew.com/all-this/2015/10/getting-those-apollo-photos-from-flickr/)
			and the FlickrAPI (https://stuvel.eu/flickrapi-doc/)
			
"""

import sys
try:
	from flickrapi import FlickrAPI
except ImportError:
	sys.exit("You'll need to install FlickrAPI")
try:
	import requests
except ImportError:
	sys.exit("You'll need to install requests")
import json
import os

def getOriginalURL(id):
  s = flickr.photos.getSizes(photo_id=id)
  for x in s.find('sizes').getiterator():
  	if x.get('label') == "Original":
  		return x.get('source')
  return False

if not os.path.exists("./backup/"):
	os.mkdir('./backup')
	print("made the backup dir")

# Flickr parameters, these are my API keys, whatevs.
key = '888561822065aaf59f97c7028785f8a2'
secret = 'bf9520dd4e9b6bff'

flickr = FlickrAPI(key, secret, format='etree')
flickr.authenticate_via_browser(perms='read')

for photo in flickr.walk_user('me'):
	pid = photo.get('id')
	filename = '{}-{}.jpg'.format(pid, photo.get('title'))
	print(filename)
	url = getOriginalURL(pid)
	if url:
		print(url)
		if not os.path.exists('backup/{}'.format(filename)):
			img = requests.get(url)
			if img.status_code <400:
				with open('backup/{}'.format(filename), 'wb') as fh:
					fh.write(img.content)
			else:
				sys.exit("got error code {}".format(img.status_code))
		else:
			print("skipping, already exists")
	else:
		print("couldn't get original link for this, weird?")
		
print("Done!")