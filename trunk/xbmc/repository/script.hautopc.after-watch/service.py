import xbmc
import xbmcaddon
import xbmcgui
import os
import operator
from resources.lib import utilxbmc
from resources.lib import utilfile
from resources.lib import utilnet

__addon__ = xbmcaddon.Addon(id='script.hautopc.after-watch')

## UTIL
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
				m['title'] = '* %s' % utilxbmc.get_movie_title(m['movieid'])
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
		j = utilxbmc.xjson('{"jsonrpc":"2.0","method":"Player.GetItem","params":{"playerid":1,"properties":["file","title","imdbnumber","art"]},"id":1}')
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
		rate_tag = False
		recommended = False
		screen_off = False
		steps = 0
		if setting('fm_movies_manage') == '1': # move
			dest = Progress.dialog_path(self, 'fm_movies_destination')
			if dest:
				lib = os.path.dirname(self.path)
				if setting('fm_movies_structure') == '0':
					lib = os.path.dirname(os.path.dirname(self.path))
				if not dest == lib: # already watched
					move = True
					steps += self.MOVE_STEPS
		elif setting('fm_movies_manage') == '2': # delete
			delete = True
			steps += self.DELETE_STEPS
		if setting('rt_movies_imdb') == 'true' or setting('rt_movies_lib') == 'true' or setting('rt_movies_tag') == 'true':
			r = Progress.dialog_rating(self)
			if r:
				if setting('rt_movies_imdb') == 'true':
					rate_imdb = True
					steps += self.RATE_IMDB_STEPS
				if setting('rt_movies_lib') == 'true':
					rate_lib = True
					steps += self.RATE_LIB_STEPS
				if setting('rt_movies_tag') == 'true':
					rate_tag = True
					steps += self.RATE_TAG_STEPS
		if setting('rc_movies_imdb') == 'true':
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
		if rate_tag:
			if progress.start_module(lang(30517), self.RATE_TAG_STEPS):
				self.__rate_tag(progress)
			progress.finish_module()
		if recommended:
			if progress.start_module(lang(30515), self.RECOMMENDED_STEPS):
				self.__recommended(progress)
			progress.finish_module()
		# after
		if self.recommended:
			movieid = Progress.dialog_recommended(self)
			if movieid:
				utilxbmc.play_movie(movieid)
		if screen_off and not player.isPlaying():
			Progress.screen_off()

	MOVE_STEPS = 3
	def __move(self, progress):
		progress.update(lang(30506)) # moving files
		source = os.path.dirname(self.path)
		destination = os.path.normpath(setting('fm_movies_destination'))
		if setting('fm_movies_structure') == '0': # multiple folders
			if setting('fm_alternate') == 'false':
				utilfile.move_directory(source, destination)
			else:
				utilfile.copy_directory_alt(source, destination)
				utilfile.delete_directory_alt(source)
			self.path = os.path.join(destination, self.path.split(os.sep)[-2], os.path.basename(self.path))
		else: # single folder
			match = os.path.splitext(os.path.basename(self.path))[0]
			if setting('fm_alternate') == 'false':
				utilfile.move_files(source, destination, match)
			else:
				utilfile.copy_files_alt(source, destination, match)
				utilfile.delete_files_alt(source, match)
			self.path = os.path.join(destination, os.path.basename(self.path))
		progress.update(lang(30513)) # updating library
		progress.update_library()
		self.movieid = utilxbmc.get_movieid_by_path(self.path)
		if self.movieid:
			progress.update(lang(30514)) # setting watched
			utilxbmc.set_movie_watched(self.movieid)

	DELETE_STEPS = 2
	def __delete(self, progress):
		progress.update(lang(30516)) # deleting files
		path = os.path.dirname(self.path)
		f = os.path.basename(self.path)
		if setting('fm_movies_structure') == '0': # multiple folders
			if setting('fm_alternate') == 'false':
				utilfile.delete_directory(path)
			else:
				utilfile.delete_directory_alt(path)
		else: # single folder
			match = os.path.splitext(f)[0]
			if setting('fm_alternate') == 'false':
				utilfile.delete_files(path, match)
			else:
				utilfile.delete_files_alt(path, match)
		progress.update(lang(30513)) # updating library
		progress.update_library()
		self.movieid = None
		self.path = None

	RATE_IMDB_STEPS = 3
	def __rate_imdb(self, progress):
		progress.update(lang(30519)) # logging in imdb
		s = utilnet.login_imdb(setting('rt_imdb_user'), setting('rt_imdb_pass'))
		if not s:
			Progress.notification('Error: loggin in IMDb')
			return
		progress.update(lang(30520)) # rating on imdb
		s = utilnet.rate_imdb(s, self.imdb, self.rating)
		if not s:
			Progress.notification('Error: rating on IMDb')
			return
		progress.update(lang(30521)) # logging out imdb
		utilnet.logout_imdb(s)

	RATE_LIB_STEPS = 1
	def __rate_lib(self, progress):
		if not self.movieid: # todo porque isto?
			Progress.notification('Error: rate library')
			return
		progress.update(lang(30522)) # updating rating
		utilxbmc.set_movie_rating(self.movieid, self.rating)

	RATE_TAG_STEPS = 1
	def __rate_tag(self, progress):
		if not self.movieid: # todo porque isto?
			Progress.notification('Error: rate library')
			return
		progress.update(lang(30524)) # setting tag
		tag = setting('rt_movies_tag_text')
		if '%s' in tag:
			tag = tag % self.rating
		utilxbmc.set_movie_tag(self.movieid, tag)


	RECOMMENDED_STEPS = 2
	def __recommended(self, progress):
		progress.update(lang(30527)) # browsing imdb
		movies = utilnet.recommended_imdb(self.imdb)
		if not movies:
			Progress.notification('Error: recommended movies not found')
			return
		progress.update(lang(30528)) # searching library
		for movie in movies:
			movie['movieid'] = utilxbmc.get_movieid_by_imdb(movie['imdb'])
		self.recommended = movies

class Episode:
	def __init__(self):
		j = utilxbmc.xjson('{"jsonrpc":"2.0","method":"Player.GetItem","params":{"playerid":1,"properties":["file","title","art"]},"id":1}')
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
		if setting('fm_episodes_manage') == '1':
			dest = Progress.dialog_path(self, 'fm_episodes_destination')
			if dest:
				lib = os.path.dirname(os.path.dirname(os.path.dirname(self.path)))
				if not dest == lib: # already watched
					move = True
					steps += self.MOVE_STEPS
		elif setting('fm_episodes_manage') == '2':
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
		if setting('fm_alternate') == 'false':
			utilfile.move_files(source, destination, match, True)
		else:
			utilfile.copy_files_alt(source, destination, match)
			utilfile.delete_files_alt(source, match, True)
		self.path = os.path.join(destination, os.path.basename(self.path))
		progress.update(lang(30513)) # updating library
		progress.update_library()
		self.episodeid = utilxbmc.get_episodeid_by_path(self.path)
		if self.episodeid:
			progress.update(lang(30514)) # setting watched
			utilxbmc.set_episode_watched(self.episodeid)
	
	DELETE_STEPS = 2
	def __delete(self, progress):
		progress.update(lang(30516)) # deleting files
		source = os.path.dirname(self.path)
		match = os.path.splitext(os.path.basename(self.path))[0]
		if setting('fm_alternate') == 'false':
			utilfile.delete_files(source, match, True)
		else:
			utilfile.delete_files_alt(source, match, True)
		progress.update(lang(30513)) # updating library
		progress.update_library()
		self.episodeid = None
		self.path = None
		
	RATE_LIB_STEPS = 1
	def __rate_lib(self, progress):
		if not self.episodeid: # todo porque isto?
			Progress.notification('Error: rate library')
			return
		progress.update(lang(30522)) # updating rating
		utilxbmc.set_episode_rating(self.episodeid, self.rating)

## PLAYER
class AfterWatchPlayer(xbmc.Player):
	def onPlayBackStarted(self):
		self.playing = None
		j = utilxbmc.xjson('{"jsonrpc":"2.0","method":"Player.GetActivePlayers","id":1}')
		t = j['result'][0]['type']
		i = j['result'][0]['playerid']
		if t == 'video':
			j = utilxbmc.xjson('{"jsonrpc":"2.0","method":"Player.GetItem","params":{"playerid":%s},"id":1}' % i)
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
