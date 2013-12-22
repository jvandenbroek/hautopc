import re
from . import requests

def has_net():
	try:
		requests.get('http://www.google.com')
		return True
	except:
		return False

def login_imdb(username, password):
	session = requests.Session()
	session.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'})
	# read login page
	src = session.get('https://secure.imdb.com/register-imdb/login').text
	match = re.search(r'<input\stype="hidden"\sname="(\w{1,9})"\svalue="(\w{1,9})"', src)
	if not match:
		session.close()
		return
	hidden_name = str(match.group(1))
	hidden_value = str(match.group(2))
	# login
	post_data = {hidden_name: hidden_value, 'login': username, 'password': password}
	src = session.post('https://secure.imdb.com/register-imdb/login', data=post_data).text
	if not 'logout' in src:
		session.close()
		return
	return session

def logout_imdb(session):
	session.get('https://secure.imdb.com/register-imdb/logout').text
	session.close()

def rate_imdb(session, imdb, rating):
	rating = str(rating)
	# read page
	src = session.get('http://www.imdb.com/title/%s' % imdb).text
	match = re.search(r'href="/(title/%s/vote\?v=%s;k=[^"]*)"' % (imdb, rating), src)
	if not match:
		session.close()
		return
	url = 'http://www.imdb.com/%s' % match.group(1)
	# rate it :)
	src = session.get(url).text
	if not 'Your vote of %s was counted' % rating in src:
		session.close()
		return
	return session

def recommended_imdb(imdb):
	session = requests.Session()
	session.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'})
	src = session.get('http://m.imdb.com/title/%s/similarities' % imdb).text
	session.close()
	#movies = re.findall(r'(\w{9})/\?ref_=tt_rec_tti"\s><img\sheight="113"\swidth="76"\salt="([^"]*)"\stitle=', src)
	#movies = re.findall(r'(tt\d{7})/"\sonClick="_gaq\.push\(\[\'_trackEvent\',\s\'Find\',\s\'\',\s\'\']\);">(.*)</a>', src)
	movies = re.findall(r'<div class="label">\s*<div class="title">\s*<a href="/title/(tt\d{7})/">([^<]*)', src)
	movies = [{'imdb': movie[0], 'title': movie[1]} for movie in movies]
	return movies
