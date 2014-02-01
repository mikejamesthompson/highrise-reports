# coding: utf-8
import time
from datetime import datetime
import os

import smtplib
from email.mime.text import MIMEText

import config
import highriser
import utils

import sys


def getDeals():

	# Get last checked date
	lastChecked = os.path.getmtime("date-indicator")
	sinceDate = datetime.fromtimestamp(lastChecked)

	# Change modification date here
	utils.touch("date-indicator")

	# Form URL
	path = "/deals.xml"
	parameters = "?since=20131201000000"
	# parameters = "?since=" + sinceDate.strftime("%Y%m%d%H%M%S")
	url = config.DOMAIN + path + parameters

	# Get soouuup
	soup = highriser.getHighriseSoup(url)

	# We need just deals marked as won since lastChecked
	wonDeals = []

	deals = soup.findAll('deal')

	for deal in deals:
		
		# Extract date of any status change for comparison 
		if(deal.find('status-changed-on').string):
			statusChanged = deal.find('status-changed-on').string
		else:
			statusChanged = "1970-01-01"
		
		dateStatusChanged = datetime.strptime(statusChanged, '%Y-%m-%d')

		if(dateStatusChanged >= datetime.strptime("2013-12-01", '%Y-%m-%d')):
			# Won deals
			if(deal.status.string == 'won'):
				wonDeals.append(highriser.formatDealData(deal))
		else:
			continue

	emailAlerts(wonDeals)

	return wonDeals


def emailAlerts(deals):
	
	for deal in deals:
		message = MIMEText(deal['name'] + "\n\n" + deal['background'] + "\n\nCategory: " + deal['category'] + "\nOwner: " + deal['owner'])
		message['Subject']='We\'ve won ' + deal['name']+u', worth: £'+deal['value']+'!'
		message['From'] = 'mike@mysociety.org'
		message['To'] = 'mike@mysociety.org'

		s = smtplib.SMTP('localhost')
		s.sendmail('bounce@mysociety.org', ['mike@mysociety.org'], message.as_string())
		s.quit()

	return True


if __name__ == "__main__":

	print getDeals()
