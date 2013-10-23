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