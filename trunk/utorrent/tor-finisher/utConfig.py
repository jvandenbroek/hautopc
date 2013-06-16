import os
import sys
import re
import time
import xml.etree.ElementTree as xml
from lib import requests

try:
	# find himself
	if getattr(sys, 'frozen', False):
		PROGRAM_PATH = os.path.dirname(sys.executable)
	else:
		PROGRAM_PATH = os.path.dirname(__file__)

	# parse settings from file
	SETTINGS_PATH = os.path.join(PROGRAM_PATH, 'settings.xml')
	if not os.path.exists(SETTINGS_PATH):
		raise Exception('Settings file not found (%s)' % SETTINGS_PATH)
	SETTINGS = xml.parse(SETTINGS_PATH).getroot()
	UTORRENT_HOST = SETTINGS.find('utorrent/server/host').text
	UTORRENT_PORT = SETTINGS.find('utorrent/server/port').text
	UTORRENT_USER = SETTINGS.find('utorrent/server/username').text
	UTORRENT_PASS = SETTINGS.find('utorrent/server/password').text

	# retrieve token from utorrent
	print 'Connecting to uTorrent...'
	s = requests.session()
	AUTH = requests.auth.HTTPBasicAuth(UTORRENT_USER, UTORRENT_PASS)
	URL = 'http://%s:%s/gui/token.html' % (UTORRENT_HOST, UTORRENT_PORT)
	HEADERS = {'content-type': 'application/json', 'user-agent': 'python-requests'}
	try:
		r = s.get(URL, headers=HEADERS, auth=AUTH)
	except:
		raise Exception('Cant connect to uTorrent. Probably wrong settings or uTorrent not running.')
	REGEX = r'<div[^>]*id=[\"\']token[\"\'][^>]*>([^<]*)</div>'
	MATCH = re.search(REGEX, r.text, re.IGNORECASE)
	if not MATCH:
		raise Exception('Cant connect to uTorrent')
	TOKEN = MATCH.group(1)

	# set setting in utorrent
	print 'Updating "Run when finish" setting in uTorrent...'
	URL = 'http://%s:%s/gui/' % (UTORRENT_HOST, UTORRENT_PORT)
	LINE = '"' + os.path.join(PROGRAM_PATH, 'TorFinisher.exe') + '" "%L" "%N" "%D" "%K" "%F" "%I"'
	PARAMS = {'token': TOKEN, 'action': 'setsetting', 's': 'finish_cmd', 'v': LINE}
	r = s.get(URL, headers=HEADERS, auth=AUTH, params=PARAMS)
	if not 'build' in r.json():
		raise Exception('Cant set setting in uTorrent')
except Exception, e:
	print e.message
	time.sleep(10)
else:
	print 'Sucess!'
	time.sleep(5)
