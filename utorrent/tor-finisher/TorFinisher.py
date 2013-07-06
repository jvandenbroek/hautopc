import sys
import os
import shutil
import re
import json
import time
import xml.etree.ElementTree as xml
import unicodedata
import Tkinter
import tkMessageBox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from lib import requests
from lib import disks

## INFO
PROGRAM_NAME = 'Tor Finisher'
PROGRAM_VERSION = '1.0.0'
PROGRAM_ICON = 'https://code.google.com/p/hautopc/source/browse/trunk/utorrent/tor-finisher/logo.png'
if getattr(sys, 'frozen', False):
	PROGRAM_PATH = os.path.dirname(sys.executable)
else:
	PROGRAM_PATH = os.path.dirname(__file__)

## ARGUMENTS
# START /MIN "C:\path\to\TorFinisher.exe" "%L" "%N" "%D" "%K" "%F" "%I"
if not len(sys.argv) == 7:
	Tkinter.Tk().wm_withdraw()
	tkMessageBox.showerror(PROGRAM_NAME, 'Incorrect number of arguments')
	sys.exit()
TORRENT_LABEL = sys.argv[1]
TORRENT_TITLE = sys.argv[2]
TORRENT_PATH = sys.argv[3]
TORRENT_KIND = sys.argv[4]
TORRENT_FILE = sys.argv[5]
TORRENT_HEX = sys.argv[6]

## SETTINGS
path = os.path.join(PROGRAM_PATH, 'settings.xml')
if not os.path.exists(path):
	Tkinter.Tk().wm_withdraw()
	tkMessageBox.showerror(PROGRAM_NAME, 'Settings not found\n%s' % path)
	sys.exit()
settings = xml.parse(path).getroot()

## CONSTANTS
ENABLED = settings.find('enabled').text
MOVIES_PATH = settings.find('processing/library/movieslocation').text
SERIES_PATH = settings.find('processing/library/serieslocation').text
MOVIES_LABEL = settings.find('processing/utorrent/movieslabel').text
SERIES_LABEL = settings.find('processing/utorrent/serieslabel').text
LABEL_SEPARATOR = settings.find('processing/utorrent/labelseparator').text
UNRAR_PATH = settings.find('processing/unrar/location').text
LOG_ENABLED = settings.find('processing/log/enabled').text
UTORRENT_HOST = settings.find('utorrent/server/host').text
UTORRENT_PORT = settings.find('utorrent/server/port').text
UTORRENT_USER = settings.find('utorrent/server/username').text
UTORRENT_PASS = settings.find('utorrent/server/password').text
UTORRENT_ENABLED = settings.find('utorrent/enabled').text
UTORRENT_DAYS_OLDER = settings.find('utorrent/conditions/daysolder').text
UTORRENT_COMPARATOR = settings.find('utorrent/conditions/comparator').text
UTORRENT_RATIO = settings.find('utorrent/conditions/ratio').text
EMAIL_ENABLED = settings.find('email/enabled').text
EMAIL_FROM = settings.find('email/headers/from').text
EMAIL_TOS = [to.text for to in settings.findall('email/headers/to/email')]
EMAIL_HOST = settings.find('email/server/host').text
EMAIL_PORT = settings.find('email/server/port').text
EMAIL_USER = settings.find('email/server/username').text
EMAIL_PASS = settings.find('email/server/password').text
XBMC_ENABLED = settings.find('xbmc/enabled').text
XBMC_HOST = settings.find('xbmc/server/host').text
XBMC_PORT = settings.find('xbmc/server/port').text
XBMC_USER = settings.find('xbmc/server/username').text
XBMC_PASS = settings.find('xbmc/server/password').text
LOG_PATH = os.path.join(PROGRAM_PATH, 'log', '%s.log' % TORRENT_TITLE)
MOVIES_FOLDERNAME = '%s (%s)'
SERIES_FOLDERNAME = '%s'
SEASON_FOLDERNAME = 'Season %s'
SERIES_INFO_FILENAME = 'tvshow.nfo'
MOVIES_INFO_FILENAME = 'movie.nfo'
INFO_EXTENSIONS = ['.nfo']
VIDEO_EXTENSIONS = ['.avi', '.mkv', '.mp4']
EXTRACT_EXTENSIONS = ['.rar']
EMAIL_SUBJECT_MOVIE = 'NEW MOVIE: %s'
EMAIL_SUBJECT_EPISODE = 'NEW EPISODE: %s'
EMAIL_SUBJECT_UNSORTED = 'NEW: %s'
EMAIL_SUBJECT_ERROR = 'ERROR: %s'
EMAIL_SUBJECT_WARNING = 'WARNING: %s'
EMAIL_LINK1 = 'http://m.imdb.com/title/%s/'
EMAIL_LINK2 = 'http://%s:%s@%s:%s/jsonrpc?request={"jsonrpc":"2.0","method":"Player.Open","params":{"item":{"file":"%s"}},"id":1}' % (XBMC_USER, XBMC_PASS, XBMC_HOST, XBMC_PORT, '%s')
INFO_CONTENT = 'http://akas.imdb.com/title/%s/'
IMDB_API_URL = 'http://imdbapi.org/?id=%s&type=xml&plot=simple&episode=0&lang=en-US&aka=simple&release=simple&business=0&tech=0'
TMDB_API_URL = 'http://api.themoviedb.org/3/movie/%s?api_key=7d67c745d7368d3046dcf716426ad79f'
POSTER_URL = 'http://d3gtl9l2a4fn1j.cloudfront.net/t/p/w185%s'
XBMC_URL = 'http://%s:%s/jsonrpc' % (XBMC_HOST, XBMC_PORT)
UTORRENT_URL = 'http://%s:%s/gui/' % (UTORRENT_HOST, UTORRENT_PORT)
UTORRENT_URL_TOKEN = '%stoken.html' % UTORRENT_URL
REGEX_IMDB_API_POSTER = r'<poster>(.+)</poster>'
REGEX_IMDB_URL = r'imdb\.com/title/(tt\d{7})'
REGEX_SERIES_TITLE = r'[^%s]*%s([^%s]+)' % (LABEL_SEPARATOR, LABEL_SEPARATOR, LABEL_SEPARATOR)
REGEX_SERIES_SEASON_EPISODE = r's0*(\d{1,2})e(\d{2})'
REGEX_SERIES_SEASON_EPISODE_ALT = r'([1-9]*\d})x(\d{2})'
REGEX_UTORRENT_TOKEN = r'<div[^>]*id=[\"\']token[\"\'][^>]*>([^<]*)</div>'
XBMC_CMD_MOVIES = '{"jsonrpc":"2.0","method":"VideoLibrary.GetMovies","params":{"properties":["file"]},"id":1}'
XBMC_CMD_EPISODES = '{"jsonrpc":"2.0","method":"VideoLibrary.GetEpisodes","params":{"properties":["file"]},"id":1}'
XBMC_CMD_UPDATE = '{"jsonrpc":"2.0","method":"VideoLibrary.Scan","id":1}'
XBMC_CMD_BUSY = '{"jsonrpc":"2.0","method":"XBMC.GetInfoBooleans","params":{ "booleans": ["library.isscanning"] },"id":1}'
XBMC_CMD_ALERT = '{"jsonrpc":"2.0","method":"GUI.ShowNotification","params":{"title":"%s","message":"%s","image":"%s","displaytime":7000},"id":1}'
UTORRENT_CMD_LIST = {'list': 1}
UTORRENT_INDEX_HASH = 0
UTORRENT_INDEX_STATUS = 1
UTORRENT_INDEX_NAME = 2
UTORRENT_INDEX_PERCENT = 4
UTORRENT_INDEX_RATIO = 7
UTORRENT_INDEX_UPSPEED = 8
UTORRENT_INDEX_LABEL = 11
UTORRENT_INDEX_ADDEDON = 23
UTORRENT_INDEX_PATH = 26
UTORRENT_BITWISE_STARTED = 1
UTORRENT_BITWISE_PAUSED = 32
UTORRENT_BITWISE_QUEUED = 64
UNRAR_OK = 'All OK'
MINIMUM_FREE_SPACE = 20

## CLASS
class Logger:
	S = '%s | %s | %s'
	def __init__(self, enabled, path):
		self.start = time.time()
		self.enabled = enabled
		self.path = path
		print PROGRAM_NAME + ' ' + PROGRAM_VERSION
		if self.enabled == 'True':
			d = os.path.dirname(path)
			if not os.path.exists(d):
				os.mkdir(d)
			self.f = open(path, 'a')
			self.f.write(PROGRAM_NAME + ' ' + PROGRAM_VERSION + '\n')

	def close(self):
		duration = int(time.time() - self.start)
		print 'Finished in %s seconds!' % duration
		if self.enabled == 'True':
			self.f.write('Finished in %s seconds!' % duration)
			self.f.close()

	def __time(self):
		return time.strftime('%Y/%m/%d %H:%M.%S', time.localtime())

	def info(self, msg):
		print self.S % (self.__time(), 'INFO', msg)
		if self.enabled == 'True':
			self.f.write('%s | INFO | %s\n' % (self.__time(), msg))

	def warning(self, msg):
		print self.S % (self.__time(), 'WARNING', msg)
		if self.enabled == 'True':
			self.f.write('%s | WARNING | %s\n' % (self.__time(), msg))
		send_email(EMAIL_SUBJECT_WARNING % TORRENT_TITLE, msg)

	def error(self, msg):
		print self.S % (self.__time(), 'ERROR', msg)
		if self.enabled == 'True':
			self.f.write('%s | ERROR | %s\n' % (self.__time(), msg))
		send_email(EMAIL_SUBJECT_ERROR % TORRENT_TITLE, msg)

## UTIL
def get_file(path, extensions, not_sample=True):
	f = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and os.path.splitext(f)[1] in extensions and (not not_sample or not 'SAMPLE' in os.path.basename(f).upper())]
	if not len(f) == 1:
		raise Exception('File %s not found in: %s' % (', '.join(extensions), path))
	return f[0]

def test_path(path, *paths):
	for p in paths:
		path = os.path.join(path, p)
	if not os.path.exists(path):
		raise Exception('Path not found: %s' % path)
	return path

def create_directory(if_necessary, path, *paths):
	for p in paths:
		path = os.path.join(path, p)
	if os.path.exists(path) and not if_necessary:
		raise Exception('Directory already exists: %s' % path)
	elif not os.path.exists(path):
		os.makedirs(path)
	return path

def create_file(content, path, *paths):
	for p in paths:
		path = os.path.join(path, p)
	f = open(path, 'w')
	f.write(content)
	f.close()
	return path

def move(path, destination):
	shutil.move(path, destination)
	path = os.path.join(destination, os.path.basename(path))
	return path

def extract(path, destination):
	if os.path.splitext(path)[1] in EXTRACT_EXTENSIONS:
		log.info('Extracting...')
		os.system('""%s" x "%s" "%s\\"' % (UNRAR_PATH, path, destination))
		f = [os.path.join(destination, f) for f in os.listdir(destination) if os.path.isfile(os.path.join(destination, f)) and not os.path.basename(f) == SERIES_INFO_FILENAME]
		if not len(f) == 1:
			raise Exception('Extracted multiple files in: %s' % destination)
		tmp_path = os.path.join(destination, os.path.basename(f[0]))
	else:
		log.info('Copying...')
		shutil.copy(path, destination)
		tmp_path = os.path.join(destination, os.path.basename(path))
	name = TORRENT_TITLE + os.path.splitext(tmp_path)[1]
	name = name.replace(' ','.')
	path = os.path.join(destination, name)
	os.rename(tmp_path, path)
	return path

def replace_special_chars(text):
	text = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
	text = text.replace('\'', '')
	text = text.replace('amp;', ' ')
	text = re.sub('[^A-Za-z0-9]+', ' ', text)
	text = re.sub('\s+', ' ', text)
	text = text.strip()
	return text

def find_in_string(string, regex):
	match = re.search(regex, string, re.IGNORECASE)
	if not match:
		raise Exception('Regex couldnt match')
	return match.groups()

def find_in_file(path, regex):
	f = open(path, 'r')
	content = f.read()
	f.close()
	return find_in_string(content, regex)

def find_in_webpage(url, regex):
	content = requests.get(url).text
	return find_in_string(content, regex)

def find_in_tmdb(id):
	headers = {'Accept': 'application/json'}
	r = requests.get(TMDB_API_URL % id, headers=headers)
	return r.json()

def access_utorrent(cmd):
	headers = {'content-type': 'application/json', 'user-agent': 'python-requests'}
	auth = requests.auth.HTTPBasicAuth(UTORRENT_USER, UTORRENT_PASS)
	r = requests.get(UTORRENT_URL_TOKEN, headers=headers, auth=auth)
	token = find_in_string(r.text, REGEX_UTORRENT_TOKEN)[0]
	guid = r.cookies['GUID']
	cookies = dict(GUID = guid)
	cmd.update({'token': token})
	r = requests.get(UTORRENT_URL, headers=headers, auth=auth, params=cmd, cookies=cookies)
	return r.json()

def access_xbmc(cmd):
	headers = {'content-type': 'application/json', 'user-agent': 'python-requests'}
	auth = requests.auth.HTTPBasicAuth(XBMC_USER, XBMC_PASS)
	params = {'request': cmd}
	r = requests.get(XBMC_URL, params=params, headers=headers, auth=auth)
	j = r.json()
	if 'error' in j:
		raise Exception('Error connecting to Xbmc')
	return j

def disk_full(disk):
	u = disks.disk_usage(disk)
	free = 100 * u[2] / u[0]
	if free <= MINIMUM_FREE_SPACE:
		return True

## SUPL
def test_episode(path, episode):
	f = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and ('E%s'%episode in os.path.basename(f).upper() or 'X%s'%episode in os.path.basename(f).upper())]
	if not len(f) == 0:
		raise Exception('Episode %s already exists in: %s' % (episode, path))

def generate_body(title, subtitle, imdb, poster, path):
	body = '<div style="width:300px;margin:0px auto;text-align:center;"><span style="display:block;margin-bottom:2px;font-size:10px;color:gray;">%TORRENT%</span><span style="display:block;margin-bottom:0px;font-size:20px;font-weight:bold;">%TITLE%</span><span style="display:block;margin-bottom:2px;font-size:12px;font-weight:bold;">%SUBTITLE%</span><table width="185" height="278" cellspacing="0" cellpadding="0" border="0" style="margin:0px auto;border-collapse:collapse;background-color:gray" background="%POSTER%"><tr height="222"><td><a href="%LINK1%"><div style="width:185px;height:220px;"></div></a></td></tr><tr height="56"><td style="background-color:rgba(222,222,222,0.5);"><a href="%LINK2%"><img width="41" height="41" style="padding-top:7px;padding-bottom:3px;padding-left:72px;padding-right:72px;" src="http://mba.terry.uga.edu/_assets/img/playButton2.png" alt="play"/></a></td></tr></table></div>'
	body = body.replace('%TORRENT%', TORRENT_TITLE)
	body = body.replace('%TITLE%', title)
	body = body.replace('%SUBTITLE%', subtitle)
	body = body.replace('%LINK1%', EMAIL_LINK1 % imdb)
	body = body.replace('%POSTER%', poster)
	body = body.replace('%LINK2%', EMAIL_LINK2 % path.replace('\\','/'))
	return body

def pause_torrents():
	log.info('Pausing torrents...')
	j = access_utorrent(UTORRENT_CMD_LIST)
	for t in j['torrents']:
		if (not t[UTORRENT_INDEX_PERCENT] == 1000 and
			t[UTORRENT_INDEX_STATUS] & UTORRENT_BITWISE_QUEUED and
			not t[UTORRENT_INDEX_STATUS] & UTORRENT_BITWISE_PAUSED):
			hash = t[UTORRENT_INDEX_HASH]
			cmd = {'action': 'pause', 'hash': hash}
			access_utorrent(cmd)

def unpause_torrents():
	log.info('Unpausing torrents...')
	j = access_utorrent(UTORRENT_CMD_LIST)
	for t in j['torrents']:
		if (not t[UTORRENT_INDEX_PERCENT] == 1000 and
			t[UTORRENT_INDEX_STATUS] & UTORRENT_BITWISE_PAUSED):
			hash = t[UTORRENT_INDEX_HASH]
			cmd = {'action': 'unpause', 'hash': hash}
			access_utorrent(cmd)

def remove_torrents():
	if UTORRENT_ENABLED == 'True':
		log.info('Removing torrents...')
		epoch = int(time.time() - int(UTORRENT_DAYS_OLDER)*24*60*60)
		j = access_utorrent(UTORRENT_CMD_LIST)
		for t in j['torrents']:
			if (not t[UTORRENT_INDEX_NAME] == TORRENT_TITLE and
				(t[UTORRENT_INDEX_LABEL].startswith(LABEL_MOVIES) or t[UTORRENT_INDEX_LABEL].startswith(LABEL_SERIES)) and
				t[UTORRENT_INDEX_PERCENT] == 1000 and
				t[UTORRENT_INDEX_UPSPEED] == 0 and
				t[UTORRENT_INDEX_ADDEDON] < epoch and
				((UTORRENT_COMPARATOR == 'lesser' and t[UTORRENT_INDEX_RATIO] < UTORRENT_RATIO) or
				(UTORRENT_COMPARATOR == 'greater' and t[UTORRENT_INDEX_RATIO] > UTORRENT_RATIO))):
				hash = t[UTORRENT_INDEX_HASH]
				cmd = {'action': 'removedata', 'hash': hash}
				access_utorrent(cmd)
				log.info('Torrent deleted: %s' % t[UTORRENT_INDEX_NAME])

def update_movies_xbmc(path):
	if XBMC_ENABLED == 'True':
		log.info('Updating xbmc...')
		movies = access_xbmc(XBMC_CMD_MOVIES)['result']['movies']
		before = len(movies)
		exist = [movie for movie in movies if movie['file'] == path]
		if exist:
			raise Exception('Movie already in XBMC library')
		access_xbmc(XBMC_CMD_UPDATE)
		time.sleep(0.2)
		while access_xbmc(XBMC_CMD_BUSY)['result']['library.isscanning']:
			time.sleep(0.2)
		movies = access_xbmc(XBMC_CMD_MOVIES)['result']['movies']
		exist = [movie for movie in movies if movie['file'] == path]
		if not exist:
			raise Exception('Movie not added to XBMC library')
		after = len(movies)
		if not before+1 == after:
			raise Exception('Inconsistent number of movies in XBMC library')

def update_episodes_xbmc(path):
	if XBMC_ENABLED == 'True':
		log.info('Updating xbmc...')
		episodes = access_xbmc(XBMC_CMD_EPISODES)['result']['episodes']
		before = len(episodes)
		exist = [episode for episode in episodes if episode['file'] == path]
		if exist:
			raise Exception('Episode already in XBMC library')
		access_xbmc(XBMC_CMD_UPDATE)
		time.sleep(0.2)
		while access_xbmc(XBMC_CMD_BUSY)['result']['library.isscanning']:
			time.sleep(0.2)
		episodes = access_xbmc(XBMC_CMD_EPISODES)['result']['episodes']
		exist = [episode for episode in episodes if episode['file'] == path]
		if not exist:
			raise Exception('Episode not added to XBMC library')
		after = len(episodes)
		if not before+1 == after:
			raise Exception('Inconsistent number of episodes in XBMC library')

def notify_xbmc(title, message, image):
	access_xbmc(XBMC_CMD_ALERT % (title, message, image))

def send_email(subject, body):
	if EMAIL_ENABLED == 'True':
		log.info('Sending email...')
		msg = MIMEMultipart('alternative')
		msg['Subject'] = subject
		msg['From'] = EMAIL_FROM
		msg['To'] = ', '.join(EMAIL_TOS)
		msg.attach(MIMEText(body, 'html'))
		s = SMTP(EMAIL_HOST, EMAIL_PORT)
		s.starttls()
		s.login(EMAIL_USER, EMAIL_PASS)
		s.sendmail(EMAIL_FROM, EMAIL_TOS, msg.as_string())
		s.quit()
		log.info('Email sent to: %s' % ', '.join(EMAIL_TOS))

## PROCCESSING
def process_movie():
	log.info('Processing movie...')
	# pause torrents
	pause_torrents()
	# check disks space and remove torrents
	try:
		d1 = os.path.splitdrive(TORRENT_PATH)[0]
		d2 = os.path.splitdrive(MOVIES_PATH)[0]
		if disk_full(d1) or disk_full(d2):
			remove_torrents()
			if disk_full(d1) or disk_full(d2):
				raise Exception('Disk %s or %s full' % (d1, d2))
	except Exception, e:
		log.warning(e.message)
	# process files and data
	try:
		# get nfo and rar or video files from torrent directory
		torrent_info = get_file(TORRENT_PATH, INFO_EXTENSIONS)
		log.info('Torrent info file: %s' % torrent_info)
		torrent_video = get_file(TORRENT_PATH, VIDEO_EXTENSIONS+EXTRACT_EXTENSIONS)
		log.info('Torrent video/extract file: %s' % torrent_video)
		# get imdb from nfo
		movie_imdb = find_in_file(torrent_info, REGEX_IMDB_URL)[0]
		log.info('Imdb: %s' % movie_imdb)
		# get title and year from tmdb
		tmdb = find_in_tmdb(movie_imdb)
		movie_title = tmdb['original_title']
		movie_year = tmdb['release_date'][:4]
		log.info('Title: %s | Year: %s' % (movie_title, movie_year))
		movie_title = replace_special_chars(movie_title)
		# create directory in library
		movie_path = create_directory(False, MOVIES_PATH, MOVIES_FOLDERNAME % (movie_title, movie_year))
		# copy or extract and rename movie to library
		movie_video_path = extract(torrent_video, movie_path)
		log.info('Library video file: %s' % movie_video_path)
		# create nfo in library
		movie_info_path = create_file(INFO_CONTENT % movie_imdb, movie_path, MOVIES_INFO_FILENAME)
		log.info('Library info file: %s' % movie_info_path)
	except Exception, e:
		log.error(e.message)
	else:
		try:
			# update xbmc
			update_movies_xbmc(movie_video_path)
			notify_xbmc('New Movie', movie_title, PROGRAM_ICON)
			# send email
			movie_poster = POSTER_URL % tmdb['poster_path']
			body = generate_body(movie_title, movie_year, movie_imdb, movie_poster, movie_video_path)
			send_email(EMAIL_SUBJECT_MOVIE % movie_title, body)
		except Exception, e:
			log.warning(e.message)
	# start torrents
	unpause_torrents()

def process_episode():
	log.info('Processing episode...')
	# pause torrents
	pause_torrents()
	# check disks space and remove torrents
	try:
		d1 = os.path.splitdrive(TORRENT_PATH)[0]
		d2 = os.path.splitdrive(SERIES_PATH)[0]
		if disk_full(d1) or disk_full(d2):
			remove_torrents()
			if disk_full(d1) or disk_full(d2):
				raise Exception('Disk %s or %s full' % (d1, d2))
	except Exception, e:
		log.warning(e.message)
	# process files and data
	try:
		# get rar or video files from torrent directory
		torrent_video = get_file(TORRENT_PATH, VIDEO_EXTENSIONS+EXTRACT_EXTENSIONS)
		log.info('Torrent video/extract file: %s' % torrent_video)
		# get title, season and episode from file
		serie_title = find_in_string(TORRENT_LABEL, REGEX_SERIES_TITLE)[0]
		try:
			serie_season, serie_episode = find_in_string(TORRENT_TITLE, REGEX_SERIES_SEASON_EPISODE)
		except:
			serie_season, serie_episode = find_in_string(TORRENT_TITLE, REGEX_SERIES_SEASON_EPISODE_ALT)
		log.info('Title: %s | Season: %s | Episode: %s' % (serie_title, serie_season, serie_episode))
		# check if serie directory and nfo exist in library
		serie_path = test_path(SERIES_PATH, SERIES_FOLDERNAME % serie_title)
		serie_info = get_file(serie_path, INFO_EXTENSIONS)
		log.info('Library info file: %s' % serie_info)
		# create season directory if necessary
		serie_season_path = create_directory(True, serie_path, SEASON_FOLDERNAME % serie_season)
		# check if episode doesnt exist
		test_episode(serie_season_path, serie_episode)
		# copy or extract and rename episode to tmp
		serie_video_path = extract(torrent_video, serie_path)
		# move episode file to season directory
		serie_video_path = move(serie_video_path, serie_season_path)
		log.info('Library video file: %s' % serie_video_path)
	except Exception, e:
		log.error(e.message)
	else:
		try:
			# update xbmc
			update_episodes_xbmc(serie_video_path)
			notify_xbmc('New Episode', serie_title, PROGRAM_ICON)
			# send email
			serie_imdb = find_in_file(serie_info, REGEX_IMDB_URL)[0]
			log.info('Imdb: %s' % serie_imdb)
			serie_poster = find_in_webpage(IMDB_API_URL % serie_imdb, REGEX_IMDB_API_POSTER)
			body = generate_body(serie_title, '%sx%s'%(serie_season,serie_episode), serie_imdb, serie_poster, serie_video_path)
			send_email(EMAIL_SUBJECT_EPISODE % serie_title, body)
		except Exception, e:
			log.warning(e.message)
	# start torrents
	unpause_torrents()

def process_unsorted():
	log.info('Processing unsorted...')
	# check disks space and remove torrents
	try:
		d = os.path.splitdrive(TORRENT_PATH)[0]
		if disk_full(d):
			remove_torrents()
			if disk_full(d):
				raise Exception('Disk %s full' % d)
	except Exception, e:
		log.warning(e.message)
	# inform user
	try:
		send_email(EMAIL_SUBJECT_UNSORTED % TORRENT_TITLE, TORRENT_TITLE)
	except Exception, e:
		log.warning(e.message)

## MAIN
try:
	if ENABLED == 'True':
		log = Logger(LOG_ENABLED, LOG_PATH)
		log.info('Torrent label: %s' % TORRENT_LABEL)
		log.info('Torrent title: %s' % TORRENT_TITLE)
		log.info('Torrent path: %s' % TORRENT_PATH)
		log.info('Torrent kind: %s' % TORRENT_KIND)
		log.info('Torrent file: %s' % TORRENT_FILE)
		log.info('Torrent hex: %s' % TORRENT_HEX)
		if TORRENT_LABEL.startswith(MOVIES_LABEL):
			process_movie()
		elif TORRENT_LABEL.startswith(SERIES_LABEL):
			process_episode()
		else:
			process_unsorted()
		log.close()
		time.sleep(3)
except Exception, e:
	Tkinter.Tk().wm_withdraw()
	tkMessageBox.showerror(PROGRAM_NAME, 'CRITICAL ERROR\n' + TORRENT_TITLE + '\n' + e.message)
