============
Installation
============

**pillowncase** has been written in Python 3.5 and tested on Windows 10 and Ubuntu 16.04 LTS.

.. _install_ubuntu:

-----------------------------
Installation Ubuntu 16.04 LTS
-----------------------------

	Ubuntu comes with several versions of python installed including 3.5 but defaults to 2.7, it is recommended that you set up a Python virtual environment (in general not just for this) to run pillowncase.
	Virtual environments are very easy to set up and keeps everything nicely isolated.

	1. Create a directory for your virtual environment (you can call it whatever you like but we are going to use pillowncase so I don't have to type everything out twice for the development environment setup).

		::
		
		$ mkdir pillowncase

	2. pillowncase has two dependencies 'pillow' and 'cryptography'.
		
		The pip installer will automatically download these however to build cryptography some additional files are required on this version of Ubuntu or it will fail so before we get started lets get those installed first.::

		$ sudo apt-get install build-essential libssl-dev libffi-dev python-dev python3.dev

	Accept default Y for all, you can also refer to the `cryptography install guide <https://cryptography.io/en/latest/installation/>`_. for additional information on dependencies.

	3. Now we need to install the virtual environment creation tool, this will let us create and manage virtual environments.

		::

		$ sudo apt-get install python-virtualenv

	4. Make sure you are in the directory you created, in this case pillowncase and create an environment.

		All the code is doing is saying copy the relevant parts from the python install located at */usr/bin/python3.5* and put them in a new sub folder of pillowncase called .env.
		If you wanted to create a 2.7 environment for example you could just create a new directory and rerun with */usr/bin/python2.7* and it would copy that.::

			$ cd pillowncase
			$ virtualenv -p /usr/bin/python3.5 .env
			
		Check there is now a hidden directory called .env created.  You can call the directory whatever you like but it's easiest to pick one name and stick with it as you will see in a sec.::

			$ ls -lart
			drwxr-xr-x 27 mark mark 4096 Dec 31 19:09 ..
			drwxrwxr-x  3 mark mark 4096 Dec 31 19:33 .
			drwxrwxr-x  6 mark mark 4096 Dec 31 19:33 .env


		Now start the virtual environment, this just makes sure that your path is updated so the relevant python commands default to your virtual environment.  Assuming your Ubuntu python path is set at it's default you can see this working.

		Just run python with out doing anything to test default system install note it.s 2.7.::

			$ python
			Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
			[GCC 5.4.0 20160609] on linux2
			Type "help", "copyright", "credits" or "license" for more information.
			>>> quit()

		Now activate your virtual environment.

		First note the python version when you run python it's now 3.5

		Second note you now have (.env) at the start of your command prompt to remind you that environment is the one you are in.::

			$ source .env/bin/activate
			(.env) mark@computername:~/pillowncase$ python
			Python 3.5.2 (default, Nov 17 2016, 17:05:23) 
			[GCC 5.4.0 20160609] on linux
			Type "help", "copyright", "credits" or "license" for more information.
			>>> quit()

		To deactivate your virtual environment just type deactivate and you will see the (.env) vanish..::

			(.env) mark@computername:~/pillowncase$ deactivate

		To save trying *source .env/bin/activate* every time it's easy to alias it in your bash shell, just add the following line to the end of your .bashrc file
		and next time you start a new terminal you can just type activate (when you are in the virtual environment directory) this is another reason to keep
		all the virtual environment directory's the same name you can just use activate each time.::

			alias activate='source .env/bin/activate'

		.. warning:: Make sure your virtual environment is running check you have a (.env) in front of your command line when installing else you will install into your default python which most likely won't break anything but will soon become cluttered.

	5. Now we can install pillowncase, make sure you are in your virtual python instance and it is activated.

		::

			       $ pwd
			       $ ~/pillowncase
			       $ activate
			(.env) $ pip install pillowncase

		That should be all there is to it, pillowncase will download along with the dependences.

	6. Test it installed ok, create a test image called pNcase_small_test.png

		::

			(.env) $ python -m pillowncase
			::encode::
			::Reading Datafile: /home/mark/pncase/.env/lib/python3.5/site-packages/pillowncase/files/pNcase_test.txt
			::Resizing Image to fit to data
			::Writing data to Image
			::Progress: 100%
			::Image 'pNcase_small_test.png'' created and saved

		Now get the hidden data out a test file called pNcase_test.txt

		::

			(.enc) $ python -m pillowncase -a decode -i pNcase_small_test.png
			::Decode::
			::Opened Imagefile: pNcase_small_test.png
			::Reading data from Image
			::Progress: 100%::Found hidden file: pNcase_test.txt
			::Sucesfuly read data
			::All done Data Written to file: pNcase_test.txt

	7. Refer to the rest of the documentation on all the available methods and how to use fully.



-----------------------
Installation Windows 10
-----------------------

	Windows does not come with Python installed, if you don't have it installed install 3.5 from the main `python site <https://www.python.org/downloads/>`_.

	It is recommended that you set up a Python virtual environment (in general not just for this) to run pillowncase.
	Virtual environments are very easy to set up and keeps everything nicely isolated, this install guide will step you through the process.

	1. Open powershell (just type powershell where it says Ask me anything)

	2. Create a directory for your virtual environment, you can call it anything I'm calling it pillowncase

		::

			PS C:\Users\mark> mkdir pillowncase

		    Directory: C:\Users\mark

			Mode                LastWriteTime         Length Name
			----                -------------         ------ ----
			d-----       31/12/2016     20:37                pillowncase

	3. Install the virtual environment creation tool using pip (this will install it in your default Python thats fine)

		::

			PS C:\Users\mark> pip install virtualenv

	4. Change to your new directory and create a virtual Python environment, all this command is doing is copying the parts it needs from your python install to make a clean virtual environment.

		If you have multiple Python environments installed you can just select the one you want, in my case I'm choosing 3.5, update the path to reflect your install.::

			PS C:\Users\mark> cd .\pillowncase\
			PS C:\Users\mark\pillowncase> virtualenv -p 'C:\Users\mark\AppData\Local\Programs\Python\Python35\python.exe' .env

		All the above has done is created a directory called .env and moved all the relevant scripts in there.

	5. Activate the virtual environment.

		Because of windows security it won't let you run scripts by default in powershell even if they are signed so you need to elevate the privileges.
		Right click on the powershell icon and select run as administrator this will open a new powershell command prompt, now run the following, I selected All
		but pick the one that you are happy with.  You can read the official explanation on the `virtualenv site <https://virtualenv.pypa.io/en/stable/userguide/>`_.
		however the recommendation there of using AllSigned did not work for me on windows 10 you only have to do this once but be aware of the implications.::

			PS C:\Users\mark\pillowncase> Set-ExecutionPolicy RemoteSigned

		You don't need to run as admin any more, close all powershell prompts and reopen one.  Now you should be able to activate your virtual environment as follows, note you get a leading (.env) on your command prompt as a visual aid that you are in the virtual python environment.::

			PS C:\Users\mark> .\.env\Scripts\activate
			(.env) PS C:\Users\mark> python
			Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:18:55) [MSC v.1900 64 bit (AMD64)] on win32
			Type "help", "copyright", "credits" or "license" for more information.
			>>> quit()

		To quite the environment type deactivate you will see the (.env) vanish.::

			(.env) PS C:\Users\mark\pillowncase> deactivate 
			PS C:\Users\mark\pillowncase>

		.. warning:: Make sure your virtual environment is running check you have a (.env) in front of your command line when installing else you will install into your default python which most likely won't break anything but will soon become cluttered.


	6. Now we can install pillowncase, make sure you are in your virtual python instance and it is activated.

		::

			PS C:\Users\mark> .\.env\Scripts\activate
			(.env) PS C:\Users\mark> pip install pillowncase

		That should be all there is to it, pillowncase will download along with the dependences.

	7. Test it installed ok, create a test image called pNcase_small_test.png

		::

			(.env) PS C:\Users\mark3\pillowncase> python -m pillowncase
			::encode::
			::Reading Datafile: /home/mark/pncase/.env/lib/python3.5/site-packages/pillowncase/files/pNcase_test.txt
			::Resizing Image to fit to data
			::Writing data to Image
			::Progress: 100%
			::Image 'pNcase_small_test.png'' created and saved

		Now get the hidden data out a test file called pNcase_test.txt

		::

			(.enc) PS C:\Users\mark3\pillowncase> python -m pillowncase -a decode -i pNcase_small_test.png
			::Decode::
			::Opened Imagefile: pNcase_small_test.png
			::Reading data from Image
			::Progress: 100%::Found hidden file: pNcase_test.txt
			::Sucesfuly read data
			::All done Data Written to file: pNcase_test.txt

	8. Refer to the rest of the documentation on all the available methods and how to use fully.