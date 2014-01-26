from lib import requests
import re
import os
import shutil
import sys
import time
import pickle
import Tkinter
import tkMessageBox

PROGRAM_NAME = 'Tor Grabber'
PROGRAM_VERSION = '1.0.0'
PROGRAM_DEV = 'Pynto R'
PROGRAM_EMAIL = 'r.pynto@gmail.com'
PROGRAM_SITE = 'https://code.google.com/p/hautopc/'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'


class Torrent(object):
	def __init__(self, sublink, times):
		self.times = int(times)
		self.link = 'http://torrentleech.org%s' % sublink
		self.filename = self.link.split('/')[-1]
		self.title = self.filename.split('.torrent')[0]
		self.title2 = self.title.replace('.',' ')

	def __eq__(self, other):
		return self.link == other.link

	def __ne__(self, other):
		return not self.__eq__(other)

	def qualifies(self):
		if (settings['min_times'] < self.times and
		settings['word'] in self.title and
		not settings['not_word'] in self.title):
			return True
		else:
			return False


## EXCEPTIONS
class LoginException(Exception):
	pass

class SiteException(Exception):
    pass


## GRAPHICS
line = 79 * '-'
dline = 79 * '='

def clear():
	os.system('cls')
	print dline
	print '%s %s - %s' % (PROGRAM_NAME, PROGRAM_VERSION, PROGRAM_SITE)
	print '%s (%s)' % (PROGRAM_DEV, PROGRAM_EMAIL)
	print dline













# import requests
# import re

# UTORRENT_URL = 'http://%s:%s/gui/' % ('192.168.1.80', '55655')
# UTORRENT_URL_TOKEN = '%stoken.html' % UTORRENT_URL
# REGEX_UTORRENT_TOKEN = r'<div[^>]*id=[\"\']token[\"\'][^>]*>([^<]*)</div>'


# auth = requests.auth.HTTPBasicAuth('HauToPC', 'nas2htpc')
# headers = {'content-type': 'application/json'}
# r = requests.get(UTORRENT_URL_TOKEN, auth=auth, headers=headers)
# token = re.search(REGEX_UTORRENT_TOKEN, r.text).group(1)
# guid = r.cookies['GUID']
# cookies = dict(GUID = guid)

# headers = {'content-type': 'multipart/form-data'}
# params = {'action':'add-file','token': token}
# #files = {'torrent_file':'C:\\x.torrent'}
# files = {'torrent_file': open('C:\\x.torrent', 'rb')}
# r = requests.post(UTORRENT_URL, auth=auth, cookies=cookies, headers=headers, params=params, files=files)
# print r.json()





## MENUS
def scan():
	clear()
	try:
		log_torrents = []
		countdown = 0
		error = 0
		while True:
			clear()
			print 'Scanning in %s minutes...' % countdown
			print 'Press CTRL + C to stop'
			print line
			if countdown == 0:
				countdown = settings['refresh']
				# create session and login
				session = requests.Session()
				session.headers.update({'User-Agent': USER_AGENT})
				post_data = {'username': settings['username'], 'password': settings['password']}
				src = session.post('http://torrentleech.org/user/account/login/', data=post_data).text
				if 'Invalid Username/password combination' in src:
					raise LoginException()
				# get site torrents
				try:
					src = session.get(settings['url']).text
				except:
					pass
				sublinks = re.findall(r'<td class="quickdownload">\s+<a href="(/download/[^"]+)">', src)
				times = re.findall(r'<td>(\d+)<br>times</td>', src)
				total = len(sublinks)
				if total == 0:
					error += 1
				else:
					error = 0
				# scroll through torrents and check conditions
				for i in xrange(total):
					torrent = Torrent(sublinks[i], times[i])
					if torrent.qualifies():
						if torrent not in log_torrents:
							log_torrents.append(torrent)
							# download torrent
							d = session.get(torrent.link, stream=True)
							filename = os.path.join(settings['path'], torrent.filename)
							with open(filename, 'wb') as out:
								shutil.copyfileobj(d.raw, out)
							del d
				session.close()
			else:
				countdown -= 1
			if error == 3:
				raise SiteException()
			for torrent in log_torrents:
				print torrent.title2
			time.sleep(60)
	except LoginException:
		session.close()
		print 'Invalid username/password'
		time.sleep(3)
	except SiteException:
		session.close()
		Tkinter.Tk().wm_withdraw()
		tkMessageBox.showerror(PROGRAM_NAME, 'Cant connect to TL')
	except KeyboardInterrupt:
		pass

def set_string_setting(setting):
	clear()
	print 'Current: %s' % settings[setting]
	settings[setting] = raw_input('    New: ')

def set_int_setting(setting):
	clear()
	print 'Current: %s' % settings[setting]
	i = raw_input('    New: ')
	if i.isdigit():
		settings[setting] = int(i)

def exit():
	with open('settings.obj', 'w') as f:
		pickle.dump(settings, f)
	sys.exit()


## START
try:
	with open('settings.obj', 'r') as f:
		settings = pickle.load(f)
except:
	settings = {'username':'', 'password':'', 'url':'http://torrentleech.org/torrents/browse/index/categories/13',
				'refresh':30, 'min_times':200, 'word':'.720p.', 'not_word':'.RC.', 'path':''}

while True:
	clear()
	print '1. Scan!'
	print '2. Settings'
	print '0. Exit'
	print line
	option = raw_input('Select option [0-2]: ')
	if option.isdigit():
		if option == '1':
			scan()
		elif option == '2':
			while True:
				clear()
				print '1. Set TL username'
				print '2. Set TL password'
				print '3. Set TL category url'
				print '4. Set scan refresh time'
				print '5. Set torrent minimum times downloaded'
				print '6. Set torrent contain word'
				print '7. Set torrent not contain word'
				print '8. Set download path'
				print '0. [Back]'
				print line
				option = raw_input('Select option [0-11]: ')
				if option.isdigit():
					if option == '1':
						set_string_setting('username')
					elif option == '2':
						set_string_setting('password')
					elif option == '3':
						set_string_setting('url')
					elif option == '4':
						set_int_setting('refresh')
					elif option == '5':
						set_int_setting('min_times')
					elif option == '6':
						set_string_setting('word')
					elif option == '7':
						set_string_setting('not_word')
					elif option == '8':
						set_string_setting('path')
					elif option == '0':
						break
		elif option == '0':
			exit()
