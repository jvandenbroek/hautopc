import xbmc
import xbmcaddon
import xbmcgui
import os
import operator
from resources.lib import utilfile
from resources.lib import utilnet
from resources.lib import utilxbmc


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


## DIALOG
def dialog_proceed(title, subtitle):
	proceed = True
	if setting('confirm') == 'true':
		proceed = xbmcgui.Dialog().yesno(info('name'), title, lang(30526) % subtitle)
	return proceed

def dialog_error(msg):
	xbmcgui.Dialog().ok(info('name'), msg)

def dialog_notification(msg):
	xbmc.executebuiltin('Notification(%s,%s,5000,%s)' % (info('name'), msg, info('icon')))
	# todo xbmcgui.Dialog().notification('Movie Trailers', 'Finding Nemo download finished.', xbmcgui.NOTIFICATION_INFO, 5000)

def dialog_rating(title):
	l = ['10 **********','9 *********','8 ********','7 *******','6 ******','5 *****','4 ****','3 ***','2 **','1 *']
	i = xbmcgui.Dialog().select(lang(30512) % (info('name'), title), l)
	if not i == -1:
		rating = 10 - i
		return rating

def dialog_recommended(playing):
	movies = playing.recommended
	for m in movies:
		if m['movieid']:
			m['title'] = '* %s' % utilxbmc.get_movie_title(m['movieid'])
	movies = sorted(movies, key=operator.itemgetter('title'))
	i = xbmcgui.Dialog().select(lang(30509) % info('name'), [m['title'] for m in movies])
	#l = xbmcgui.ListItem('foobar')
	if not i == -1:
		return movies[i]['movieid']


## PROGRESS
class Progress:
	def __init__(self, steps):
		self.enable = setting('hide_progress') == 'false' # todo temp
		self.steps = steps
		self.current = 0
		if steps > 0 and self.enable: # todo temp
			if utilxbmc.version() == 13: # todo temp
				self.bar = xbmcgui.DialogProgressBG()
			else: # todo temp
				self.bar = xbmcgui.DialogProgress() # todo temp
			self.bar.create(info('name'))
			self.bar.update(0, info('name'))

	def start_module(self, module_title, module_steps):
		self.module_title = module_title
		self.module_steps = module_steps
		self.module_current = 0
	
	def update(self, msg):
		percent = self.current * 100 / self.steps
		if self.enable: # todo temp
			self.bar.update(percent, info('name'), lang(30531) % (self.module_title, msg))
		self.current += 1
		self.module_current += 1

	def finish_module(self):
		if not self.module_steps == self.module_current:
			skip = self.module_steps - self.module_current
			self.current += skip
			self.module_current += skip
		percent = self.current * 100 / self.steps
		if self.current == self.steps:
			if self.enable: # todo temp
				self.bar.update(percent, info('name'), 'Done')
				xbmc.sleep(500)
				self.bar.close()

	def update_library(self):
		xbmc.executebuiltin('CleanLibrary(video)')
		while not xbmc.getCondVisibility('Library.IsScanningVideo'):
			pass
		while xbmc.getCondVisibility('Library.IsScanningVideo'):
			xbmc.sleep(20)
		#self.bar.close()
		#self.bar = None
		xbmc.executebuiltin('UpdateLibrary(video)')
		while not xbmc.getCondVisibility('Library.IsScanningVideo'):
			pass
		while xbmc.getCondVisibility('Library.IsScanningVideo'):
			xbmc.sleep(20)
		percent = (self.current-1) * 100 / self.steps
		#self.bar = xbmcgui.DialogProgressBG()
		#self.bar.create(info('name'))
		self.bar.update(percent, info('name'),  lang(30531) % (self.module_title, lang(30513)))


## TYPES
class Video:
	def show_quit_menu(self):
		xbmc.executebuiltin('ActivateWindow(shutdownmenu)')

	def logoff_user(self):
		xbmc.executebuiltin('System.LogOff')

	def turn_display_off(self):
		#if os.name == 'nt': and not player.isPlaying():
		path = xbmc.translatePath('special://home/addons/script.hautopc.after-watch/resources/lib/Sleeper.exe')
		os.startfile(path)


class Movie(Video):
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

	MOVE_STEPS = 3
	def __move(self, progress):
		progress.start_module(lang(30132), self.MOVE_STEPS)
		try:
			lib_destiny = os.path.normpath(setting('fm_movies_destination'))
			if setting('fm_movies_structure') == '0':
				lib_source = os.path.dirname(os.path.dirname(self.path))
		 	else:
		 		lib_source = os.path.dirname(self.path)
		 	if lib_destiny == lib_source:
		 		raise Exception(lang(30607))
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
		except Exception, e:
			dialog_error(e.message)
		finally:
			progress.finish_module()

	DELETE_STEPS = 2
	def __delete(self, progress):
		progress.start_module(lang(30133), self.DELETE_STEPS)
		try:
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
		except Exception, e:
			dialog_error(e.message)
		finally:
			progress.finish_module()

	RATE_IMDB_STEPS = 3
	def __rate_imdb(self, progress):
		progress.start_module(lang(30201), self.RATE_IMDB_STEPS)
		try:
			if not utilnet.has_net():
				raise Exception(lang(30608))
			progress.update(lang(30519)) # logging in imdb
			s = utilnet.login_imdb(setting('rt_imdb_user'), setting('rt_imdb_pass'))
			if not s:
				raise Exception(lang(30605))
			progress.update(lang(30520)) # rating on imdb
			s = utilnet.rate_imdb(s, self.imdb, self.rating)
			if not s:
				raise Exception(lang(30606))
			progress.update(lang(30521)) # logging out imdb
			utilnet.logout_imdb(s)
		except Exception, e:
			dialog_error(e.message)
		finally:
			progress.finish_module()

	RATE_LIB_STEPS = 1
	def __rate_lib(self, progress):
		progress.start_module(lang(30204), self.RATE_LIB_STEPS)
		try:
			if not self.movieid:
				raise Exception(lang(30604))
			progress.update(lang(30522)) # updating rating
			utilxbmc.set_movie_rating(self.movieid, self.rating)
		except Exception, e:
			dialog_error(e.message)
		finally:
			progress.finish_module()

	RATE_TAG_STEPS = 1
	def __rate_tag(self, progress):
		progress.start_module(lang(30205), self.RATE_TAG_STEPS)
		try:
			if not self.movieid:
				raise Exception(lang(30604))
			progress.update(lang(30524)) # setting tag
			tag = setting('rt_movies_tag_text')
			if '%s' in tag:
				tag = tag % self.rating
			utilxbmc.set_movie_tag(self.movieid, tag)
		except Exception, e:
			dialog_error(e.message)
		finally:
			progress.finish_module()

	RECOMMENDED_STEPS = 2
	def __recommended(self, progress):
		progress.start_module(lang(30301), self.RECOMMENDED_STEPS)
		try:
			progress.update(lang(30527)) # browsing imdb
			movies = utilnet.recommended_imdb(self.imdb)
			if not movies:
				raise Exception(lang(30603))
			progress.update(lang(30528)) # searching library
			for movie in movies:
				movie['movieid'] = utilxbmc.get_movieid_by_imdb(movie['imdb'])
			self.recommended = movies
		except Exception, e:
			dialog_error(e.message)
		finally:
			progress.finish_module()

	def ended(self):
		# pre confirm
		steps = 0
		move = False
		delete = False
		rate_imdb = False
		rate_lib = False
		rate_tag = False
		recommended = False
		if setting('fm_movies_manage') == '1': # move
			if dialog_proceed(self.title, lang(30132)):
				move = True
				steps += self.MOVE_STEPS
		elif setting('fm_movies_manage') == '2': # delete
			if dialog_proceed(self.title, lang(30133)):
				delete = True
				steps += self.DELETE_STEPS
		if setting('rt_movies_imdb') == 'true':
			if dialog_proceed(self.title, lang(30201)):
				rate_imdb = True
				steps += self.RATE_IMDB_STEPS
		if setting('rt_movies_lib') == 'true':
			if dialog_proceed(self.title, lang(30204)):
				rate_lib = True
				steps += self.RATE_LIB_STEPS
		if setting('rt_movies_tag') == 'true':
			if dialog_proceed(self.title, lang(30205)):
				rate_tag = True
				steps += self.RATE_TAG_STEPS
		if setting('rc_movies_imdb') == 'true':
			if dialog_proceed(self.title, lang(30301)):
				recommended = True
				steps += self.RECOMMENDED_STEPS
		# pre settings
		if move:
			destiny = os.path.normpath(setting('fm_movies_destination'))
			while not destiny or destiny == '.':
				destiny = xbmcgui.Dialog().browse(3, lang(30525) % info('name'), 'files')
				destiny = os.path.normpath(destiny)
			set_setting('fm_movies_destination', destiny)
		if rate_imdb:
			user = setting('rt_imdb_user')
			while not user:
				user = xbmcgui.Dialog().input(lang(30529) % (info('name')))
			set_setting('rt_imdb_user', user)
			password = setting('rt_imdb_pass')
			while not password:
				password = xbmcgui.Dialog().input(lang(30555) % info('name'), option=xbmcgui.ALPHANUM_HIDE_INPUT)
			set_setting('rt_imdb_pass', password)
		if rate_tag:
			tag = setting('rt_movies_tag_text')
			while not tag:
				tag = xbmcgui.Dialog().input(lang(30206))
			set_setting('rt_movies_tag_text', tag)
		# pre context
		if rate_imdb or rate_lib or rate_tag:
			rating = dialog_rating(self.title)
			while not rating:
				rating = dialog_rating(self.title)
			self.rating = rating
		# pre process
		progress = Progress(steps)
		if move:
			self.__move(progress)
		elif delete:
			self.__delete(progress)
		if rate_imdb:
			self.__rate_imdb(progress)
		if rate_lib:
			self.__rate_lib(progress)
		if rate_tag:
			self.__rate_tag(progress)
		if recommended:
			self.__recommended(progress)

		# process
		if self.recommended:
			movieid = dialog_recommended(self)
			if movieid:
				utilxbmc.play_movie(movieid)

		# post confirm
		quit_menu = False
		logoff = False
		display_off = False
		if setting('ps_quit_menu') == 'true':
			if dialog_proceed(self.title, lang(30402)):
				quit_menu = True
		if setting('ps_logoff') == 'true':
			if dialog_proceed(self.title, lang(30407)):
				logoff = True
		if setting('ps_display_off') == 'true':
			if dialog_proceed(self.title, lang(30404)):
				display_off = True
		# post processing
		if quit_menu:
			self.show_quit_menu()
		if logoff:
			self.logoff_user()
		if display_off:
			self.turn_display_off()


class Episode(Video):
	def __init__(self):
		j = utilxbmc.xjson('{"jsonrpc":"2.0","method":"Player.GetItem","params":{"playerid":1,"properties":["file","title","art"]},"id":1}')
		self.type = 'episode'
		self.episodeid = j['result']['item']['id']
		p = j['result']['item']['file']
		self.path = os.path.normpath(p)
		self.title = j['result']['item']['title']
		self.thumb = j['result']['item']['art']['thumb']
		self.rating = None

	MOVE_STEPS = 3
	def __move(self, progress):
		progress.start_module(lang(30132), self.MOVE_STEPS)
		try:
			lib_destiny = os.path.normpath(setting('fm_episodes_destination'))
	 		lib_source = os.path.dirname(os.path.dirname(os.path.dirname(self.path)))
		 	if lib_destiny == lib_source:
		 		raise Exception(lang(30602))
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
			if self.episodeid: # if still in lib source folders
				progress.update(lang(30514)) # setting watched
				utilxbmc.set_episode_watched(self.episodeid)
		except Exception, e:
			dialog_error(e.message)
		finally:
			progress.finish_module()
	
	DELETE_STEPS = 2
	def __delete(self, progress):
		progress.start_module(lang(30133), self.DELETE_STEPS)
		try:
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
		except Exception, e:
			dialog_error(e.message)
		finally:
			progress.finish_module()
		
	RATE_LIB_STEPS = 1
	def __rate_lib(self, progress):
		progress.start_module(lang(30204), self.RATE_LIB_STEPS)
		try:
			if not self.episodeid:
				raise Exception(lang(30601))
			progress.update(lang(30522)) # updating rating
			utilxbmc.set_episode_rating(self.episodeid, self.rating)
		except Exception, e:
			dialog_error(e.message)
		finally:
			progress.finish_module()

	def ended(self):
		# pre confirm
		steps = 0
		move = False
		delete = False
		rate_lib = False
		if setting('fm_episodes_manage') == '1': # move
			if dialog_proceed(self.title, lang(30132)):
				move = True
				steps += self.MOVE_STEPS
		elif setting('fm_episodes_manage') == '2': # delete
			if dialog_proceed(self.title, lang(30133)):
				delete = True
				steps += self.DELETE_STEPS
		if setting('rt_episodes_lib') == 'true':
			if dialog_proceed(self.title, lang(30204)):
				rate_lib = True
				steps += self.RATE_LIB_STEPS
		# pre settings
		if move:
			destiny = os.path.normpath(setting('fm_episodes_destination'))
			while not destiny or destiny == '.':
				destiny = xbmcgui.Dialog().browse(3, lang(30525) % info('name'), 'files')
				destiny = os.path.normpath(destiny)
			set_setting('fm_episodes_destination', destiny)
		 # pre context
		if rate_lib:
			rating = dialog_rating(self.title)
			while not rating:
				rating = dialog_rating(self.title)
			self.rating = rating
		# pre process
		progress = Progress(steps)
		if move:
			self.__move(progress)
		elif delete:
			self.__delete(progress)
		if rate_lib:
			self.__rate_lib(progress)

		# post confirm
		quit_menu = False
		logoff = False
		display_off = False
		if setting('ps_quit_menu') == 'true':
			if dialog_proceed(self.title, lang(30402)):
				quit_menu = True
		if setting('ps_logoff') == 'true':
			if dialog_proceed(self.title, lang(30407)):
				logoff = True
		if setting('ps_display_off') == 'true':
			if dialog_proceed(self.title, lang(30404)):
				display_off = True
		# post processing
		if quit_menu:
			self.show_quit_menu()
		if logoff:
			self.logoff_user()
		if display_off:
			self.turn_display_off()


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
