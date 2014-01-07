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