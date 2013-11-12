import re
from . import requests

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
