# Released under the GNU General Public License version 3 by J2897.

title = 'TOR Updater'
print 'Running:		' + title

def msg_box(message, box_type):
	import win32api
	user_input = win32api.MessageBox(0, message, title, box_type)
	return user_input

def stop():
	import sys
	sys.exit()

# Check if 7-Zip is installed...
import os
# sz_exe = os.getenv('PROGRAMFILES') + '\\7-Zip\\7z.exe'
# if not os.path.isfile(sz_exe):
	# print 'File not found:		' + sz_exe
	# msg_box('You don\'t appear to have 7-Zip installed. So there\'s no point proceeding to check the website for a newer version because 7-Zip is required for decompression. Please install 7-Zip and then try again.', 0)
	# stop()

target = 'Microsoft Windows'
url = 'https://www.torproject.org/projects/torbrowser.html.en'
file_url = 'https://www.torproject.org/dist/torbrowser/'
print 'Target:			' + target
print 'URL:			' + url

def get_page(page):
	import urllib2
	source = urllib2.urlopen(page)
	return source.read()

try:
	page = get_page(url)
except:
	page = None
else:
	print 'Got page...'

if page == None:
	msg_box('Could not download the page. You may not be connected to the internet.', 0)
	stop()

def find_site_ver(page):
	T1 = page.find(target)
	if T1 == -1:
		return None, None

	site_ver_start = page.find('(', T1)
	site_ver_end = page.find(')', site_ver_start)
	site_ver = page[site_ver_start+1:site_ver_end]

	T2 = page.find(site_ver+'/', site_ver_end)	
	T3 = page.find('/', T2)
	T4 = page.find('>', T3)
	return page[T3+1:T4-1], site_ver	# tor-browser-2.3.25-6_en-US.exe, 3.2.1

try:
	site_version, site_num = find_site_ver(page)
except:
	msg_box('Could not search the page.', 0)
	stop()

if site_version == None:
	msg_box('The search target has not been found on the page. The formatting, or the text on the page, may have been changed.', 0)
	stop()

print 'Found:			' + site_version

home = os.getenv('USERPROFILE')
tmp = os.getenv('TEMP') + '\\'
DL = tmp + site_version
PC = home + '\\TOR_Updater.dat'
#sz_command = [sz_exe, 'x', '-o' + home + '\\Programs\\',	tmp + site_version,	'^-y', '>', 'nul']

def dump(PC, version):
	import cPickle
	with open(PC, 'wb') as pickle_file:
		cPickle.dump(version, pickle_file)

def load():
	import cPickle
	with open(PC, 'rb') as pickle_file:
		return cPickle.load(pickle_file)

def sub_proc():
	import subprocess
	p = subprocess.Popen(DL, shell=True, stdout = subprocess.PIPE)
	stdout, stderr = p.communicate()
	return p.returncode # is 0 if success

def download_install(first_time):
	try:
		import urllib
		urllib.urlretrieve(file_url + site_num + '/' + site_version, tmp + site_version)
	except:
		msg_box('Could not download the file.', 0)
		stop()
	else:
		print 'Downloaded:		' + site_version

	try:
		RC = sub_proc()
		if RC == 0:
			if first_time:
				print 'Installation successful!'
				msg_box('Successfully installed the TOR Browser Bundle for the first time.', 0)
			else:
				print 'Update successful!'
	except:
		msg_box('Failed to execute" ' + site_version + '".', 0)
		stop()

	try:
		dump(PC, site_version)
	except:
		msg_box('Could not dump the site version information to: ' + PC, 0)
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
	first_time = True
	download_install(first_time)
	print 'Ending...'
	delay(5)
	stop()

# Load contents of Pickle Cache file (local_version).
print 'Loading cache...'
local_version = load()

def clean(text):
	import re
	return re.sub('[^0-9]', '', text)

# Are the local_version numbers the same as the site_version numbers?
clean_local_version = clean(local_version)
clean_site_version = clean(site_version)

print 'Local version:		' + clean_local_version
print 'Site version:		' + clean_site_version

if clean_local_version == clean_site_version:
	# Yes:	Quit.
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
	user_input = msg_box('There is a new version of the TOR Browser Bundle available. Please close TOR and press \'OK\' to continue.', 1)
	if user_input == 1:
		pass
	elif user_input == 2:
		stop()

# Download and install TOR, dump site_version and quit.
first_time = False
download_install(first_time)
print 'Ending...'
delay(5)
