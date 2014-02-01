import requests
from bs4 import BeautifulSoup

from datetime import datetime, time
import calendar

import config
import sys


def getHighriseSoup(url):

	# Set request parameters
	headers = {'User-Agent': config.USER_AGENT}
	auth = (config.AUTH_TOKEN,'x')

	# Fetch XML
	response = requests.get(url, auth = auth, headers = headers)
	
	if(response.status_code != requests.codes.ok):
		sys.exit('Request failed')

	return BeautifulSoup(response.text, 'xml')


def getMetadata():

	# Get users
	soup = getHighriseSoup(config.DOMAIN + "/users.xml")
	users = soup.findAll('user')
	userDict = {}

	for user in users:
		userDict[unicode(user.find('id').string)] = unicode(user.find('name').string)


	# Get categories
	soup = getHighriseSoup(config.DOMAIN + "/deal_categories.xml")
	categories = soup.findAll('deal-category')
	categoriesDict = {}

	for category in categories:
		categoriesDict[unicode(category.find('id').string)] = unicode(category.find('name').string)


	# Get tags
	soup = getHighriseSoup(config.DOMAIN + "/tags.xml")
	tags = soup.findAll('tag')
	tagsDict = {}

	for tag in tags:
		tagsDict[unicode(tag.find('id').string)] = unicode(tag.find('name').string)	

	return userDict, categoriesDict, tagsDict


def formatDealData(deal):
	"""
	Take a soupy representation of a deal and transform it into a dictionary of the values we need
	"""

	# Date formatting
	dateCreated = unicode(deal.find('created-at').string)
	dateCreated = datetime.strptime(dateCreated, '%Y-%m-%dT%H:%M:%SZ')
	dateCreated = datetime.strftime(dateCreated, '%Y-%m-%d')

	# This bit makes use of dictionaries defined in the config module to map category ids
	# and responsible party ids to their names
	d = {'name': unicode(deal.find('name').string),
		'status': unicode(deal.find('status').string),
		'status_changed': unicode(deal.find('status-changed-on').string),
		'background': unicode(deal.find('background').string),
		'value': unicode(deal.find('price').string),
		'category': unicode(categories[deal.find('category-id').string]),
		'owner': unicode(users[deal.find('responsible-party-id').string]),	
		'date_created': dateCreated
		}

	return d