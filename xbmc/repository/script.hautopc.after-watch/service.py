import xbmc
import xbmcaddon
import xbmcgui
import os
import shutil
import json
import re
import operator
from resources.lib import requests

__addon__ = xbmcaddon.Addon(id='script.hautopc.after-watch')

## UTIL XBMC
def log(msg):
	xbmc.log('[%s] %s' % (info('name'), msg))

def info(id):
	return __addon__.getAddonInfo(id)
	
def lang(id):
	return  __addon__.getLocalizedString(id)

def setting(id):
	return __addon__.getSetting(id)

def set_setting(id, val):
	__addon__.setSetting(id, val)

def xbmc_json(cmd):
	r = xbmc.executeJSONRPC(cmd)
	j = json.loads(r)
	return j

def get_movieid_by_path(path):
	j = xbmc_json('{"jsonrpc":"2.0","method":"VideoLibrary.GetMovies","params":{"properties":["file"]},"id":1}')
	if 'movies' in j['result']:
		for movie in j['result']['movies']:
			if movie['file'] == path:
				return movie['movieid']

def get_movieid_by_imdb(imdb):
	j = xbmc_json('{"jsonrpc":"2.0","method":"VideoLibrary.GetMovies","params":{"properties":["imdbnumber"]},"id":1}')
	if 'movies' in j['result']:
		for movie in j['result']['movies']:
			if movie['imdbnumber'] == imdb:
				return movie['movieid']

def get_movie_title(movieid):
	j = xbmc_json('{"jsonrpc":"2.0","method":"VideoLibrary.GetMovieDetails","params":{"movieid":%s,"properties":["title"]},"id":1}' % movieid)
	return j['result']['moviedetails']['title']

def get_episodeid_by_path(path):
	j = xbmc_json('{"jsonrpc":"2.0","method":"VideoLibrary.GetEpisodes","params":{"properties":["file"]},"id":1}')
	if 'episodes' in j['result']:
		for episode in j['result']['episodes']:
			if episode['file'] == path:
				return episode['episodeid']

def set_movie_watched(movieid):
	cmd = '{"jsonrpc":"2.0","method":"VideoLibrary.SetMovieDetails","params":{"movieid":%d,"playcount":1},"id":1}' % movieid
	xbmc.executeJSONRPC(cmd)

def set_episode_watched(episodeid):
	cmd = '{"jsonrpc":"2.0","method":"VideoLibrary.SetEpisodeDetails","params":{"episodeid":%d,"playcount":1},"id":1}' % episodeid
	xbmc.executeJSONRPC(cmd)

def set_movie_rating(movieid, rating):
	cmd = '{"jsonrpc":"2.0","method":"VideoLibrary.SetMovieDetails","params":{"movieid":%d,"rating":%s},"id":1}' % (movieid, str(rating))
	xbmc.executeJSONRPC(cmd)
	
def set_episode_rating(episodeid, rating):
	cmd = '{"jsonrpc":"2.0","method":"VideoLibrary.SetEpisodeDetails","params":{"episodeid":%d,"rating":%s},"id":1}' % (episodeid, str(rating))
	xbmc.executeJSONRPC(cmd)

def set_movie_tag(movieid, tag):
	cmd = '{"jsonrpc":"2.0","method":"VideoLibrary.SetMovieDetails","params":{"movieid":%d,"tag":["%s"]},"id":1}' % (movieid, tag)
	xbmc.executeJSONRPC(cmd)
	
def play_movie(movieid):
	cmd = '{"jsonrpc":"2.0","method":"Player.Open","params":{"item":{"movieid":%d}},"id":1}' % movieid
	xbmc.executeJSONRPC(cmd)

## UTIL FILE MANAGEMENT
def move_directory(source, destination):
	shutil.move(source,destination)

def move_files(source, destination, match, del_empty=False):
	count_source = 0
	count_match = 0
	# create directories if needed
	if not os.path.isdir(destination):
		os.makedirs(destination)
	# move files from source to destination if match
	for f in os.listdir(source):
		if match in f:
			shutil.move(os.path.join(source, f), destination)
			count_match += 1
		count_source += 1
	# delete source directory if empty
	if del_empty and count_source == count_match:
		os.rmdir(source)

def delete_directory(source):
	shutil.rmtree(source)

def delete_files(source, match):
	count_source = 0
	count_match = 0
	# delete files from source if match
	for f in os.listdir(source):
		if match in f:
			os.remove(os.path.join(source, f))
			count_match += 1
		count_source += 1
	# delete source directory if empty
	if count_source == count_match:
		os.rmdir(source)

## UTIL NET
def login_imdb(username, password):
	s = requests.Session()
	s.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31'})
	# read login page
	src = s.get('https://secure.imdb.com/register-imdb/login').text
	match = re.search(r'<input\stype="hidden"\sname="(\w{1,9})"\svalue="(\w{1,9})"', src)
	if not match:
		s.close()
		return
	hidden_name = str(match.group(1))
	hidden_value = str(match.group(2))
	# login
	post_data = {hidden_name: hidden_value, 'login': username, 'password': password}
	src = s.post('https://secure.imdb.com/register-imdb/login', data=post_data).text
	if not 'logout' in src:
		s.close()
		return
	return s

def logout_imdb(s):
	s.get('https://secure.imdb.com/register-imdb/logout').text
	s.close()

def rate_imdb(s, imdb, rating):
	rating = str(rating)
	# read page
	src = s.get('http://www.imdb.com/title/%s' % imdb).text
	match = re.search(r'href="/(title/%s/vote\?v=%s;k=[^"]*)"' % (imdb, rating), src)
	if not match:
		s.close()
		return
	url = 'http://www.imdb.com/%s' % match.group(1)
	# rate it :)
	src = s.get(url).text
	if not 'Your vote of %s was counted' % rating in src:
		s.close()
		return
	return s

def recommended_imdb(imdb):
	s = requests.Session()
	s.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31'})
	src = s.get('http://m.imdb.com/title/%s/similarities' % imdb).text
	s.close()
	#movies = re.findall(r'(\w{9})/\?ref_=tt_rec_tti"\s><img\sheight="113"\swidth="76"\salt="([^"]*)"\stitle=', src)
	movies = re.findall(r'(tt\d{7})/"\sonClick="_gaq\.push\(\[\'_trackEvent\',\s\'Find\',\s\'\',\s\'\']\);">(.*)</a>', src)
	movies = [{'imdb': movie[0], 'title': movie[1]} for movie in movies]
	return movies

## UI
class Progress:
	def __init__(self, playing, steps):
		self.enable = setting('progress') == 'true'
		self.playing = playing
		self.steps = steps
		self.current = 0
		if steps > 0 and self.enable:
			self.dialog = xbmcgui.DialogProgress()
			self.dialog.create(info('name'), self.playing.title)
			self.dialog.update(0, self.playing.title)

	def start_module(self, module_title, module_steps):
		self.module_title = module_title
		self.module_steps = module_steps
		self.module_current = 0
		proceed = self.__dialog_proceed()
		return proceed
	
	def update(self, msg):
		percent = self.current * 100 / self.steps
		if self.enable:
			self.dialog.update(percent, self.playing.title, self.module_title, msg)
		self.current += 1
		self.module_current += 1

	def finish_module(self):
		if not self.module_steps == self.module_current:
			skip = self.module_steps - self.module_current
			self.current += skip
			self.module_current += skip
		percent = self.current * 100 / self.steps
		if self.enable:
			self.dialog.update(percent, self.playing.title)
		if self.current == self.steps:
			if self.enable:
				self.dialog.close()
			Progress.notification('Done')

	def update_library(self):
		if self.enable:
			self.dialog.close()
		self.dialog = None
		xbmc.executebuiltin('CleanLibrary(video)')
		while not xbmc.getCondVisibility('Library.IsScanningVideo'):
			pass
		while xbmc.getCondVisibility('Library.IsScanningVideo'):
			xbmc.sleep(20)
		percent = (self.current-1) * 100 / self.steps
		if self.enable:
			self.dialog = xbmcgui.DialogProgress()
			self.dialog.create(info('name'), self.playing.title)
			self.dialog.update(percent, self.playing.title, self.module_title, lang(30513))
		xbmc.executebuiltin('UpdateLibrary(video)')
		while not xbmc.getCondVisibility('Library.IsScanningVideo'):
			pass
		while xbmc.getCondVisibility('Library.IsScanningVideo'):
			xbmc.sleep(20)

	def __dialog_proceed(self):
		proceed = True
		if setting('confirm') == 'true':
			proceed = xbmcgui.Dialog().yesno(info('name'), self.playing.title, lang(30526) % self.module_title)
		return proceed
	
	@staticmethod
	def dialog_path(playing, key):
		path = setting(key)
		if not path:
			path = xbmcgui.Dialog().browse(3, lang(30525)  % (info('name'), playing.title), 'video')
			set_setting(key, path)
		return os.path.normpath(path)

	@staticmethod
	def dialog_rating(playing):
		l = ['10 **********','9 *********','8 ********','7 *******','6 ******','5 *****','4 ****','3 ***','2 **','1 *']
		i = xbmcgui.Dialog().select(lang(30512) % (info('name'), playing.title), l)
		if not i == -1:
			rating = 10 - i
			playing.rating = rating
			return rating

	@staticmethod
	def dialog_recommended(playing):
		movies = playing.recommended
		for m in movies:
			if m['movieid']:
				m['title'] = '* %s' % get_movie_title(m['movieid'])
		movies = sorted(movies, key=operator.itemgetter('title'))
		i = xbmcgui.Dialog().select(lang(30509) % info('name'), [m['title'] for m in movies])
		if not i == -1:
			return movies[i]['movieid']
	
	@staticmethod
	def notification(msg):
		xbmc.executebuiltin('Notification(%s,%s,5000,%s)' % (info('name'), msg, info('icon')))
	
	@staticmethod
	def screen_off():
		if os.name == 'nt':
			path = xbmc.translatePath('special://home/addons/script.hautopc.after-watch/resources/lib/Sleeper.exe')
			os.startfile(path)

## TYPES
class Movie:
	def __init__(self):
		j = xbmc_json('{"jsonrpc":"2.0","method":"Player.GetItem","params":{"playerid":1,"properties":["file","title","imdbnumber","art"]},"id":1}')
		self.type = 'movie'
		self.movieid = j['result']['item']['id']
		p = j['result']['item']['file']
		self.path = os.path.normpath(p)
		self.title = j['result']['item']['title']
		self.imdb = j['result']['item']['imdbnumber']
		self.poster = j['result']['item']['art']['poster']
		self.rating = None
		self.recommended = None

	def ended(self):
		# pre
		move = False
		delete = False
		rate_imdb = False
		rate_lib = False
		recommended = False
		screen_off = False
		steps = 0
		if setting('fm_movies') == '1': # move
			dest = Progress.dialog_path(self, 'fm_movies_destination')
			if dest:
				lib = os.path.dirname(self.path)
				if setting('fm_movies_structure') == '0':
					lib = os.path.dirname(os.path.dirname(self.path))
				if not dest == lib: # already watched
					move = True
					steps += self.MOVE_STEPS
		elif setting('fm_movies') == '2': # delete
			delete = True
			steps += self.DELETE_STEPS
		if setting('rt_movies_imdb') == 'true' or not setting('rt_movies_lib') == '0':
			r = Progress.dialog_rating(self)
			if r:
				if setting('rt_movies_imdb') == 'true':
					rate_imdb = True
					steps += self.RATE_IMDB_STEPS
				if not setting('rt_movies_lib') == '0':
					rate_lib = True
					steps += self.RATE_LIB_STEPS
		if setting('rc_movies') == 'true':
			recommended = True
			steps += self.RECOMMENDED_STEPS
		if setting('m_screen_off') == 'true':
			screen_off = True
		# process
		progress = Progress(self, steps)
		if move:
			if progress.start_module(lang(30503), self.MOVE_STEPS):
				self.__move(progress)
			progress.finish_module()
		elif delete:
			if progress.start_module(lang(30501), self.DELETE_STEPS):
				self.__delete(progress)
			progress.finish_module()
		if rate_imdb:
			if progress.start_module(lang(30523), self.RATE_IMDB_STEPS):
				self.__rate_imdb(progress)
			progress.finish_module()
		if rate_lib:
			if progress.start_module(lang(30518), self.RATE_LIB_STEPS):
				self.__rate_lib(progress)
			progress.finish_module()
		if recommended:
			if progress.start_module(lang(30515), self.RECOMMENDED_STEPS):
				self.__recommended(progress)
			progress.finish_module()
		# after
		if self.recommended:
			movieid = Progress.dialog_recommended(self)
			if movieid:
				play_movie(movieid)
		if screen_off and not player.isPlaying():
			Progress.screen_off()

	MOVE_STEPS = 3
	def __move(self, progress):
		progress.update(lang(30506)) # moving files
		source = os.path.dirname(self.path)
		destination = os.path.normpath(setting('fm_movies_destination'))
		if setting('fm_movies_structure') == '0': # multiple folders
			destination = os.path.join(destination, self.path.split(os.sep)[-2])
			move_directory(source, destination)
		else: # single folder
			match = os.path.splitext(os.path.basename(self.path))[0]
			move_files(source, destination, match)
		progress.update(lang(30513)) # updating library
		progress.update_library()
		self.path = os.path.join(destination, os.path.basename(self.path))
		self.movieid = get_movieid_by_path(self.path)
		if self.movieid:
			progress.update(lang(30514)) # setting watched
			set_movie_watched(self.movieid)

	DELETE_STEPS = 2
	def __delete(self, progress):
		progress.update(lang(30516)) # deleting files
		path = os.path.dirname(self.path)
		f = os.path.basename(self.path)
		if setting('fm_movies_structure') == '0': # multiple folders
			delete_directory(path)
		else: # single folder
			match = os.path.splitext(f)[0]
			delete_files(path, match)
		progress.update(lang(30513)) # updating library
		progress.update_library()
		self.movieid = None
		self.path = None

	RATE_IMDB_STEPS = 3
	def __rate_imdb(self, progress):
		progress.update(lang(30519)) # logging in imdb
		s = login_imdb(setting('rt_imdb_user'), setting('rt_imdb_pass'))
		if not s:
			Progress.notification('Error: loggin in IMDb')
			return
		progress.update(lang(30520)) # rating on imdb
		s = rate_imdb(s, self.imdb, self.rating)
		if not s:
			Progress.notification('Error: rating on IMDb')
			return
		progress.update(lang(30521)) # logging out imdb
		logout_imdb(s)

	RATE_LIB_STEPS = 2
	def __rate_lib(self, progress):
		if not self.movieid:
			Progress.notification('Error: rate library')
			return
		if setting('rt_movies_lib') in ('2', '3'):
			progress.update(lang(30524)) # setting tag
			tag = setting('rt_tag')
			if '%s' in tag:
				tag = tag % self.rating
			set_movie_tag(self.movieid, tag)
		if setting('rt_movies_lib') in ('1', '3'):
			progress.update(lang(30522)) # updating rating
			set_movie_rating(self.movieid, self.rating)

	RECOMMENDED_STEPS = 2
	def __recommended(self, progress):
		progress.update(lang(30527)) # browsing imdb
		movies = recommended_imdb(self.imdb)
		if not movies:
			Progress.notification('Error: recommended movies not found')
			return
		progress.update(lang(30528)) # searching library
		for movie in movies:
			movie['movieid'] = get_movieid_by_imdb(movie['imdb'])
		self.recommended = movies

class Episode:
	def __init__(self):
		j = xbmc_json('{"jsonrpc":"2.0","method":"Player.GetItem","params":{"playerid":1,"properties":["file","title","art"]},"id":1}')
		self.type = 'episode'
		self.episodeid = j['result']['item']['id']
		p = j['result']['item']['file']
		self.path = os.path.normpath(p)
		self.title = j['result']['item']['title']
		self.thumb = j['result']['item']['art']['thumb']
		self.rating = None

	def ended(self):
		# pre
		move = False
		delete = False
		rate_lib = False
		screen_off = False
		steps = 0
		if setting('fm_episodes') == '1':
			dest = Progress.dialog_path(self, 'fm_episodes_destination')
			if dest:
				lib = os.path.dirname(os.path.dirname(os.path.dirname(self.path)))
				if not dest == lib: # already watched
					move = True
					steps += self.MOVE_STEPS
		elif setting('fm_episodes') == '2':
			delete = True
			steps += self.DELETE_STEPS
		if setting('rt_episodes_lib') == 'true':
			r = Progress.dialog_rating(self)
			if r:
				rate_lib = True
				steps += self.RATE_LIB_STEPS
		if setting('m_screen_off') == 'true':
			screen_off = True
		# process
		progress = Progress(self, steps)
		if move:
			if progress.start_module(lang(30503), self.MOVE_STEPS):
				self.__move(progress)
			progress.finish_module()
		elif delete:
			if progress.start_module(lang(30501), self.DELETE_STEPS):
				self.__delete(progress)
			progress.finish_module()
		if rate_lib:
			if progress.start_module(lang(30518), self.RATE_LIB_STEPS):
				self.__rate_lib(progress)
			progress.finish_module()
		# after
		if screen_off and not player.isPlaying():
			Progress.screen_off()
	
	MOVE_STEPS = 3
	def __move(self, progress):
		progress.update(lang(30506)) # moving files
		source = os.path.dirname(self.path)
		destination = os.path.join(os.path.normpath(setting('fm_episodes_destination')), self.path.split(os.sep)[-3], self.path.split(os.sep)[-2])
		match = os.path.splitext(os.path.basename(self.path))[0]
		move_files(source, destination, match, True)
		progress.update(lang(30513)) # updating library
		progress.update_library()
		self.path = os.path.join(destination, os.path.basename(self.path))
		self.episodeid = get_episodeid_by_path(self.path)
		if self.episodeid:
			progress.update(lang(30514)) # setting watched
			set_episode_watched(self.episodeid)
	
	DELETE_STEPS = 2
	def __delete(self, progress):
		progress.update(lang(30516)) # deleting files
		source = os.path.dirname(self.path)
		match = os.path.splitext(os.path.basename(self.path))[0]
		delete_files(source, match)
		progress.update(lang(30513)) # updating library
		progress.update_library()
		self.episodeid = None
		self.path = None
		
	RATE_LIB_STEPS = 1
	def __rate_lib(self, progress):
		if not self.episodeid:
			Progress.notification('Error: rate library')
			return
		progress.update(lang(30522)) # updating rating
		set_episode_rating(self.episodeid, self.rating)

## PLAYER
class AfterWatchPlayer(xbmc.Player):
	def onPlayBackStarted(self):
		self.playing = None
		j = xbmc_json('{"jsonrpc":"2.0","method":"Player.GetActivePlayers","id":1}')
		t = j['result'][0]['type']
		i = j['result'][0]['playerid']
		if t == 'video':
			j = xbmc_json('{"jsonrpc":"2.0","method":"Player.GetItem","params":{"playerid":%s},"id":1}' % i)
			type = j['result']['item']['type']
			if type == 'movie':
				self.playing = Movie()
				self.__time()
			elif type == 'episode':
				self.playing = Episode()
				self.__time()

	def onPlayBackEnded(self):
		if self.playing:
			self.playing.ended()
			self.playing = None

	def onPlayBackStopped(self):
		if self.playing:
			percent = self.current * 100 / self.time
			minimum = float(setting('assume'))
			if minimum <= percent:
				self.playing.ended()
			self.playing = None

	def __time(self):
		self.current = 0
		self.time = self.getTotalTime()
		if not int(setting('assume')) == 100:
			while self.isPlaying():
				self.current = self.getTime()
				xbmc.sleep(2000)

player = AfterWatchPlayer()
while not xbmc.abortRequested:
	xbmc.sleep(1000)
