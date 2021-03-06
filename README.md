TOR Updater
===========

*Released under the GNU General Public License version 3 by J2897.*

Upon first run, it will download and install the TOR Browser Bundle. All subsequent runs will check the TOR site for a newer version. If there's no newer version, it does nothing. If there is, it automatically downloads the new version and installs it. It doesn't yet verify the downloaded file's GPG signature; although I hope to implement this feature at some point in the near future.

*This has now been successfully tested on both 32-Bit and 64-Bit versions of Windows 7.*

Prerequisites
-------------

You will need the following beforehand:

* [Python] [1]
* [Python Extensions] [2]
* [TOR Updater] [3]

How to use
----------

1.	Download and install [Python 2.7.6] [1]. *Keep the default settings!*

2.	Download and install the [Python Extensions for Windows] [2]. *Keep the default settings!*

3.	Download the [master.zip] [3] file and extract the `TOR_Updater-master` folder to somewhere convenient:

		C:\Users\<name>\Updaters\TOR_Updater-master\

4.	Now launch the `Update_TOR.py` file from a Windows Command Prompt:

		C:\Python27\python.exe "C:\Users\<name>\Updaters\TOR_Updater-master\Update_TOR.py"

5.	After the installation, you may want to right-click the `Start Tor Browser.exe` file and create a shortcut on your desktop.

Automation
----------

If you've successfully installed the TOR Browser Bundle using the command in Step #4 above then you are ready to set up automation - because you probably don't want to have to manually type out that command every week or so.

There are two simple ways that you can make your PC execute that command automatically:

1.	Place a shortcut in your Startup folder. Or;
2.	Add the command to Windows Task Scheduler.

Instructions for both methods are explained below...

Place a shortcut in your Startup folder
----------------------------------------

This will run the command every time you log in to Windows. If you only log in to Windows every week or so, then this is probably your best option.

1.	First, browse Windows Explorer to your 'Startup' folder:

		C:\Users\<name>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\

2.	Browse another Windows Explorer window to your 'Python 2.7' folder:

		C:\Python27\

3.	Using your right-click button on your mouse, drag the `python.exe` file from the 'Python 2.7' folder into the 'Startup' folder.

4.	A dialogue will appear; in it, select `Create shortcuts here`.

5.	Right-click on the new `python.exe - Shortcut` file, select `Properties` and the 'Target' should currently be this:

		C:\Python27\python.exe

6.	Change that 'Target' adding the path to the `Update_TOR.py` file separated by a single space:

		C:\Python27\python.exe "C:\Users\<name>\Updaters\TOR_Updater-master\Update_TOR.py"

7.	Now click 'OK'.

The next time you log in to Windows, your PC will automatically check for - and download/install - the new version of the TOR Browser Bundle (if one is available).

Add the command to Windows Task Scheduler
-----------------------------------------

This will run the command depending on how you decide to configure Windows Task Scheduler.

*If you have placed a shortcut in your Startup folder then you do NOT need to add the command to Windows Task Scheduler!*

*If you are adding the command to Windows Task Scheduler then delete the shortcut that you placed in your Startup folder!*

1.	Open the Windows Task Scheduler:

		Control Panel > System and Security > Administrative Tools > Task Scheduler

2.	Under 'Actions' in the right-hand pane, click `Create Basic Task...` and configure as follows:

		Name:				TOR Updater
		*Configure the time as you prefer.*
		Action:				Start a program.
		Program/script:		C:\Python27\python.exe
		Add arguments:		"C:\Users\<name>\Updaters\TOR_Updater-master\Update_TOR.py"
		Start in:			C:\Python27

3.	Click 'Next', then 'Finished', and you're done!

Sandboxie tip
-------------

*Ignore this if you don't have Sandboxie installed!*

If you use Sandboxie you can create a shortcut to automatically launch your TOR Browser inside a sandbox - a good security decision considering that the person in control of the Exit Node could be someone with malicious intent.

Here's how...

1.	Right-click on your Desktop and create a new shortcut:

		New > Shortcut

2.	Select the Sandboxie executable:

		"C:\Program Files\Sandboxie\Start.exe"

3.	Name it what ever you like; 'Start Tor Browser' is fine.

4.	Right-click on the shortcut and select `Properties`.

5.	Set the 'Target' as:

		"C:\Program Files\Sandboxie\Start.exe" /box:DefaultBox /silent /nosbiectrl "C:\Users\<name>\Programs\Tor Browser\Start Tor Browser.exe"

6.	And set the 'Start in' as:

		"C:\Users\<name>\Programs\Tor Browser"

Make sure the 'Start in' is correct or else the TOR Browser will fail to open!

Issues
------

Please report any bugs [here] [4].

   [1]: http://www.python.org/ftp/python/2.7.6/python-2.7.6.msi
   [2]: http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/pywin32-219.win32-py2.7.exe/download
   [3]: https://github.com/J2897/TOR_Updater/archive/master.zip
   [4]: https://github.com/J2897/TOR_Updater/issues
