from datetime import datetime, time

import config
import highriser
import utils

import sys


def getPeople(startDate = '01 Oct 2013', endDate = '19 Nov 2013', tag=''):

	# Set dates
	quarterStart, quarterEnd = utils.setDates(startDate, endDate)

	# Form URL
	path = "/people.xml"
	parameters = ""
	if (tag != ''):
		parameters = parameters + "?tag_id=#" + str(config.TAGS[tag])
	url = config.DOMAIN + path + parameters

	print url

	# Get soouuup
	soup = highriser.getHighriseSoup(url)

	# We need contacts created in this time period
	newContacts = []

	people = soup.findAll('person')

	for person in people:

		# Extract date created for comparison later
		dateCreated = datetime.strptime(person.find('created-at').string, '%Y-%m-%dT%H:%M:%SZ')

		# New contacts
		if(dateCreated > quarterStart and dateCreated < quarterEnd):
			newContacts.append(formatPersonData(person)) 

	return newContacts


def formatPersonData(person):
	"""
	Take a soupy representation of a person and transform it into a dictionary of the values we need
	"""

	# Date formatting
	dateCreated = unicode(person.find('created-at').string)
	dateCreated = datetime.strptime(dateCreated, '%Y-%m-%dT%H:%M:%SZ')
	dateCreated = datetime.strftime(dateCreated, '%Y-%m-%d')

	# Name formatting
	firstName = unicode(person.find('first-name').string)
	lastName = unicode(person.find('last-name').string)
	
	if lastName == None:
		name = firstName + lastName
	else:
		name = firstName

	# Finding an email address
	emailAddresses = person.find('email-addresses').find_all('address')
	if(len(emailAddresses)):
		emailAddress = unicode(emailAddresses[0].string)
	else:
		emailAddress = "No email address known"

	d = {'name': name,
		'company_name': unicode(person.find('company-name').string),
		'background': unicode(person.find('background').string),
		'date_created': dateCreated,
		'email_address': emailAddress
		}

	return d


if __name__ == "__main__":
	new = getPeople('01 Sep 2013', '19 Nov 2013', 'proactive')	
	utils.writeCSV("newContacts.csv", new)
	



