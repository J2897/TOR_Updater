# Released under the GNU General Public License version 3 by J2897.

def get_page(page):
	import urllib2
	source = urllib2.urlopen(page)
	return source.read()

title = 'TOR Updater'
target = 'Tor Browser Bundle for Windows'
url = 'https://www.torproject.org/projects/torbrowser.html.en'
file_url = 'https://www.torproject.org/dist/torbrowser/'

print 'Running:		' + title
print 'Target:			' + target
print 'URL:			' + url

try:
	page = get_page(url)
except:
	page = None
else:
	print 'Got page...'

def msg_box(message, box_type):
	import win32api
	user_input = win32api.MessageBox(0, message, title, box_type)
	return user_input

def stop():
	import sys
	sys.exit()

if page == None:
	msg_box('Could not download the page. You may not be connected to the internet.', 0)
	stop()

def find_site_ver(page):
	T1 = page.find(target)
	if T1 == -1:
		return None
	T2 = page.find('tor-browser-', T1)
	T3 = page.find('>', T2)
	return page[T2:T3-1]	# tor-browser-2.3.25-6_en-US.exe

try:
	site_version = find_site_ver(page)
except:
	msg_box('Could not search the page.', 0)
	stop()
else:
	print 'Found:			' + site_version

if site_version == None:
	msg_box('The search target has not been found on the page. The formatting, or the text on the page, may have been changed.', 0)
	stop()

import os
home = os.getenv('USERPROFILE')
tmp = os.getenv('TEMP') + '\\'
DL = tmp + site_version
PC = home + '\\TOR_Updater.dat'

def clean(text):
	import re
	return re.sub('[^0-9]', '', text)

def DL_file(file_url, site_version, DL, tmp):
	import urllib
	file_url = file_url + site_version
	DL = tmp + site_version
	urllib.urlretrieve(file_url, DL)

def get_sz(tmp):
	return [os.getenv('PROGRAMFILES') + '\\7-Zip\\7z.exe', 'x', '-o' + home + '\\Programs\\',	tmp + site_version,	'^-y', '>', 'nul']

def dump(PC, version):
	import cPickle
	with open(PC, 'wb') as pickle_file:
		cPickle.dump(version, pickle_file)

def load():
	import cPickle
	with open(PC, 'rb') as pickle_file:
		return cPickle.load(pickle_file)

def sub_proc(sz_command):
	import subprocess
	p = subprocess.Popen(sz_command, shell=True, stdout = subprocess.PIPE)
	stdout, stderr = p.communicate()
	return p.returncode # is 0 if success

def download_install():
	try:
		DL_file(file_url, site_version, DL, tmp)
	except:
		msg_box('Could not download the file.', 0)
		stop()
	else:
		print 'Downloaded:		' + site_version

	try:
		sz_command = get_sz(tmp)
	except:
		msg_box('Could not construct the 7-Zip command.', 0)
		stop()

	try:
		RC = sub_proc(sz_command)
		if RC == 0:
			msg_box('Successfully updated to ' + site_version + '.', 0)
	except:
		msg_box('Failed to execute ' + site_version + '.', 0)
		stop()
	else:
		print 'Update successful!'

	try:
		dump(PC, site_version)
	except:
		msg_box('Could not dump site_version.', 0)
		stop()
	else:
		print 'Dumped cache:		' + PC

def delay(sec):
	import time
	time.sleep(sec)

# Check if the Pickle Cache file exists...
if not os.path.isfile(PC):
	# No:	Download and install TOR, create a Pickle Cache file in the home folder, dump site_version and quit.
	print 'Cache file doesn\'t exist.'
	print 'Installing TOR for the first time...'
	download_install()
	print 'Ending...'
	delay(5)
	stop()

# Load contents of Pickle Cache file (local_version).
print 'Loading cache...'
local_version = load()

# Check if the local_version numbers are in the site_version numbers...
clean_local_version = clean(local_version)
clean_site_version = clean(site_version)

if clean_local_version.find(clean_site_version) != -1:
	# Yes:	Quit.
	print 'Local version:		' + clean_local_version
	print 'Site version:		' + clean_site_version
	print 'Match!'
	print 'Ending...'
	delay(5)
	stop()

# Check if TOR is running...
def find_proc(exe):
	import subprocess
	cmd = 'WMIC PROCESS get Caption'
	proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	for line in proc.stdout:
		if line.find(exe) != -1:
			return True

while find_proc('vidalia.exe'):
	print 'TOR is running. Close TOR now!'
	user_input = msg_box('There is a new version of the TOR Browser Bundle available. Please close TOR and press OK to continue.', 1)
	if user_input == 1:
		pass
	elif user_input == 2:
		stop()

# Download and install TOR, dump site_version and quit.
download_install()
print 'Ending...'
delay(5)
