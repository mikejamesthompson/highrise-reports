from datetime import datetime, time

import config
import highriser
import utils

import sys


def getDeals(startDate = '01 Jul 2013', endDate = '30 Sep 2013'):

	# Set dates
	quarterStart, quarterEnd = utils.setDates(startDate, endDate)

	# Form URL
	path = "/deals.xml"
	parameters = "?since=" + datetime.strptime(startDate, "%d %b %Y").strftime("%Y%m%d%H%M%S")
	url = config.DOMAIN + path + parameters

	# Get soouuup
	soup = highriser.getHighriseSoup(url)

	# We need deals created in this quarter, deals won in this quarter and deals lost in this quarter
	newDeals = []
	wonDeals = []
	lostDeals = []

	deals = soup.findAll('deal')

	for deal in deals:

		# Extract date created for comparison later
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

	return (newDeals, wonDeals, lostDeals)


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
		'category': unicode(config.CATEGORIES[deal.find('category-id').string]),
		'owner': unicode(config.STAFF[deal.find('responsible-party-id').string]),	
		'date_created': dateCreated
		}

	return d


if __name__ == "__main__":
	
	new, won, lost = getDeals()	
	
	# Write contents of the three variables to three corresponding CSVs
	for segment in [("wonDeals.csv", won), ("lostDeals.csv", lost), ("newdeals.csv",new)]:
		utils.writeCSV(segment[0], segment[1])
	



