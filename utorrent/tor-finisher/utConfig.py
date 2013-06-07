import os
import sys
import re
import json
import xml.etree.ElementTree as xml
import Tkinter
import tkMessageBox
from lib import requests

def main():
	if getattr(sys, 'frozen', False):
		PROGRAM_PATH = os.path.dirname(sys.executable)
	else:
		PROGRAM_PATH = os.path.dirname(__file__)

	path = os.path.join(PROGRAM_PATH, 'settings.xml')
	if not os.path.exists(path):
		raise Exception('Settings not found\n%s' % path)
	settings = xml.parse(path).getroot()

	UTORRENT_HOST = settings.find('utorrent/server/host').text
	UTORRENT_PORT = settings.find('utorrent/server/port').text
	UTORRENT_USER = settings.find('utorrent/server/username').text
	UTORRENT_PASS = settings.find('utorrent/server/password').text
	UTORRENT_AUTH = requests.auth.HTTPBasicAuth(UTORRENT_USER, UTORRENT_PASS)
	REGEX_TOKEN = r'<div[^>]*id=[\"\']token[\"\'][^>]*>([^<]*)</div>'
	URL_API = 'http://%s:%s/gui/' % (UTORRENT_HOST, UTORRENT_PORT)
	URL_TOKEN = 'http://%s:%s/gui/token.html' % (UTORRENT_HOST, UTORRENT_PORT)
	SET = '"' + os.path.join(PROGRAM_PATH, 'TorFinisher.exe') + '" "%L" "%N" "%D" "%K" "%F" "%I"'
	HEADERS = {'content-type': 'application/json', 'user-agent': 'python-requests'}

	s = requests.session()
	r = s.get(URL_TOKEN, headers=HEADERS, auth=UTORRENT_AUTH)
	match = re.search(REGEX_TOKEN, r.text, re.IGNORECASE)
	if not match:
		raise Exception('Cant connect to utorrent')
	token = match.group(1)
	cmd = {'token': token, 'action': 'setsetting', 's': 'finish_cmd', 'v': SET}
	r = s.get(URL_API, headers=HEADERS, auth=UTORRENT_AUTH, params=cmd)
	if not 'build' in r.json():
		raise Exception('error')

if __name__ == '__main__':
	try:
		main()
	except Exception, e:
		Tkinter.Tk().wm_withdraw()
		tkMessageBox.showerror('config_ut', e.message)
		sys.exit()
	else:
		Tkinter.Tk().wm_withdraw()
		tkMessageBox.showinfo('config_ut', 'Sucess!')
