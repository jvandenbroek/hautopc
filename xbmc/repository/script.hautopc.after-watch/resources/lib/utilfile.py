import os
import shutil
import xbmcvfs

def move_directory(source, destination):
	shutil.move(source,destination)

def delete_directory(source):
	shutil.rmtree(source)

def move_files(source, destination, match, del_empty=False):
	# create directories if needed
	if not os.path.isdir(destination):
		os.makedirs(destination)
	# move files from source to destination if match
	for f in os.listdir(source):
		if match in f:
			shutil.move(os.path.join(source, f), destination)
	# delete source directory if empty
	if del_empty and len(os.listdir(source)) == 0:
		os.rmdir(source)

def delete_files(source, match, del_empty=False):
	# delete files from source if match
	for f in os.listdir(source):
		if match in f:
			os.remove(os.path.join(source, f))
	# delete source directory if empty
	if del_empty and len(os.listdir(source)) == 0:
		os.rmdir(source)

def copy_directory_alt(source, destination):
	destination = os.path.join(destination, os.path.basename(source))
	xbmcvfs.mkdirs(destination) # todo error if exists?
	dirs, files = xbmcvfs.listdir(source)
	for f in files:
		src = os.path.join(source, f)
		dest = os.path.join(destination, f)
		xbmcvfs.copy(src, dest)
	for d in dirs:
		d = os.path.join(source, d)
		copy_directory(d, destination)

def delete_directory_alt(source):
	dirs, files = xbmcvfs.listdir(source)
	for d in dirs:
		d = os.path.join(source, d)
		delete_directory(d)
	for f in files:
		f = os.path.join(source, f)
		xbmcvfs.delete(f)
	xbmcvfs.rmdir(source)

def copy_files_alt(source, destination, match):
	# create directories if needed
	xbmcvfs.mkdirs(destination)
	# move files from source to destination if match
	dirs, files = xbmcvfs.listdir(source)
	for f in files:
		if match in f:
			src = os.path.join(source, f)
			dest = os.path.join(destination, f)
			xbmcvfs.copy(src, dest) # todo error

def delete_files_alt(source, match, del_empty=False):
	# delete files from source if match
	dirs, files = xbmcvfs.listdir(source)
	for f in files:
		if match in f:
			f = os.path.join(source, f)
			xbmcvfs.delete(f)
	# delete source directory if empty
	if del_empty and len(xbmcvfs.listdir(source)) == 0:
		xbmcvfs.rmdir(source)
