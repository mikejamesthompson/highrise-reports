import time
import os.path

import config
import highriser
import utils

import sys


def getDeals():

	# Get last checked date
	lastChecked = os.path.getmtime("date-indicator")
	since = time.strftime("%Y%m%d%H%M%S", time.gmtime(time))

	# Form URL
	path = "/deals.xml"
	parameters = "?since=" + since
	url = config.DOMAIN + path + parameters

	print url
	sys.exit()

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
		if(dateCreated >= quarterStart and dateCreated <= quarterEnd):
			newDeals.append(formatDealData(deal)) 

		if(dateStatusChanged >= quarterStart and dateStatusChanged <= quarterEnd):
			# Won deals
			if(deal.status.string == 'won'):
				wonDeals.append(formatDealData(deal))
			# Lost deals
			elif(deal.status.string == 'lost'):
				lostDeals.append(formatDealData(deal))
		else:
			continue

	if(report == 'won'):
		return wonDeals
	elif(report == 'lost'):
		return lostDeals
	elif(report == 'new'):
		return newDeals
	else:
		return False


if __name__ == "__main__":
	getDeals()