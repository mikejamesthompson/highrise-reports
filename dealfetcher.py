import requests
from bs4 import BeautifulSoup

from datetime import datetime
import calendar

import csv
from unicodeutils import UnicodeWriter

import config

def formatDealData(deal):
	"""
	Take a soupy representation of a deal and transform it into a dictionary of the values we need
	"""

	# This function uses dictionaries defined in the config module to map category ids
	# and responsible party ids to their names
	d = {'name': unicode(deal.find('name').string),
		'status': unicode(deal.find('status').string),
		'status-changed': unicode(deal.find('status-changed-on').string),
		'background': unicode(deal.find('background').string),
		'value': unicode(deal.find('price').string),
		'category': unicode(config.CATEGORIES[deal.find('category-id').string]),
		'owner': unicode(config.STAFF[deal.find('responsible-party-id').string]),	
		'date_created': unicode(deal.find('created-at').string)
		}

	return d


def writeCSV(filename, deals):
	
	file = open('output/'+filename, 'wb')
	writer = UnicodeWriter(file, delimiter=',')
	
	# Write CSV column headings
	writer.writerow(deals[0].keys())
	
	# Write rows
	for d in deals:
		writer.writerow(d.values())

	file.close()
	return True


def getDeals(startDate = '01 Jul 2013'):
	
	# Set dates
	quarterStart = datetime.strptime(startDate, '%d %b %Y')
	quarterEnd = quarterStart.replace(month = quarterStart.month+2)
	quarterEnd = quarterEnd.replace(day = calendar.monthrange(quarterEnd.year, quarterEnd.month)[1])

	# Form URL
	domain = "https://mysociety.highrisehq.com"
	path = "/deals.xml"
	parameters = "?since=" + quarterStart.strftime("%Y%m%d%H%M%S")
	url = domain + path + parameters

	# Set request parameters
	headers = {'User-Agent': config.USER_AGENT}
	auth = (config.AUTH_TOKEN,'x')

	# Fetch XML
	response = requests.get(url, auth = auth, headers = headers)
	
	if(response.status_code != requests.codes.ok):
		sys.exit('Request failed')

	soup = BeautifulSoup(response.text, 'xml')

	# We need deals created in this quarter, deals won in this quarter and deals lost in this quarter
	allDeals = []
	newDeals = []
	wonDeals = []
	lostDeals = []

	deals = soup.findAll('deal')

	for deal in deals:

		allDeals.append(formatDealData(deal))

		# Extract date create for comparison later
		dateCreated = datetime.strptime(deal.find('created-at').string, '%Y-%m-%dT%H:%M:%SZ')
		
		# Extract date of any status change for comparison later
		if(deal.find('status-changed-on').string):
			statusChanged = deal.find('status-changed-on').string
		else:
			statusChanged = "1970-01-01"
		
		dateStatusChanged = datetime.strptime(statusChanged, '%Y-%m-%d')

		# New deals
		if(dateCreated > quarterStart and dateCreated < quarterEnd):
			newDeals.append(formatDealData(deal)) 

		if(dateStatusChanged > quarterStart and dateStatusChanged < quarterEnd):
			# Won deals
			if(deal.status.string == 'won'):
				wonDeals.append(formatDealData(deal))
			# Lost deals
			elif(deal.status.string == 'lost'):
				lostDeals.append(formatDealData(deal))
		else:
			continue

	# Write contents of the three variables to three corresponding CSVs
	for segment in [("allDeals.csv", allDeals), ("wonDeals.csv", wonDeals), ("lostDeals.csv", lostDeals), ("newdeals.csv",newDeals)]:
		writeCSV(segment[0], segment[1])

	return allDeals


if __name__ == "__main__":
	ds = getDeals()	
	print ds
	


