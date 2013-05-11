# Released under the GNU General Public License version 3 by J2897.

import os

def get_page(page):
	import urllib2
	source = urllib2.urlopen(page)
	return source.read()

def find_site_ver(page):
	FT = page.find(target)		# First Target
	if FT == -1:
		return None				# Remember to implement something after here.
	TB = page.find('tor-browser-', FT)	# Tor Browser
	AB = page.find('>', TB)				# Angle Bracket
	return page[TB:AB-1]				# tor-browser-2.3.25-6_en-US.exe

target = 'Tor Browser Bundle for Windows'
url = 'https://www.torproject.org/projects/torbrowser.html.en'
file_url = 'https://www.torproject.org/dist/torbrowser/'
page = get_page(url)

site_version = find_site_ver(page)
tmp = 'C:\\Users\\J2897\\AppData\\Local\\Temp\\'
DL = tmp + site_version
PC = 'C:\\Users\\J2897\\Scripts\\Python\\TOR_Updater\\pickle.dat'

def clean(text):
	import re
	return re.sub('[^0-9]', '', text)

def DL_file(file_url, site_version, DL, tmp):
	import urllib
	file_url = file_url + site_version
	DL = tmp + site_version
	urllib.urlretrieve(file_url, DL)

def get_sz(tmp, DL):
	sz_exe = '"C:\\Program Files\\7-Zip\\7z.exe\"'
	cmd = ' x'
	out = ' -o'
	Q = '"'
	prog = '"C:\\Users\\J2897\\Programs\\"'
	tmp = Q + tmp + Q
	DL = ' ' + Q + DL + Q
	OW = ' -y > nul'
	args = cmd + out + prog + DL + OW
	return sz_exe, args

def dump(PC, version):
	import cPickle
	with open(PC, 'wb') as pickle_file:
		cPickle.dump(version, pickle_file)

def load():
	import cPickle
	with open(PC, 'rb') as pickle_file:
		return cPickle.load(pickle_file)

def sub_proc(sz_exe, args):
	import subprocess
	filepath = sz_exe + args
	p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
	stdout, stderr = p.communicate()
	return p.returncode # is 0 if success

def stop():
	import sys
	sys.exit()

# Check if Pickle Cache file exists...
if not os.path.isfile(PC):
	# No:	Download and install TOR, create a Pickle Cache file in the Python Script folder, dump site_version and quit.
	DL_file(file_url, site_version, DL, tmp)
	sz_exe, args = get_sz(tmp, DL)
	sub_proc(sz_exe, args)
	dump(PC, site_version)
	stop()

# Load contents of Pickle Cache file (local_version).
local_version = load()

# Check if the local_version numbers are in the site_version numbers...
if clean(local_version).find(clean(site_version)) != -1:
	# Yes:	Quit.
	stop()

# Download and install TOR, dump site_version and quit.
DL_file(file_url, site_version, DL, tmp)
sz_exe, args = get_sz(tmp, DL)
sub_proc(sz_exe, args)
dump(PC, site_version)
