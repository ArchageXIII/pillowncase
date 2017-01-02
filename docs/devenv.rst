===============================
Install Development Environment
===============================

----------------------
Core Environment Setup
----------------------

pillowncase is hosted on github feel free to make contributions! `<https://github.com/ArchageXIII/pillowncase>`_.

I use Ubuntu for Python development so that is what this development environment setup guide is written to, it should port easily to windows.

If you want to try Ubuntu on windows pain free, follow the guide `on ask ubuntu <http://askubuntu.com/questions/142549/how-to-install-ubuntu-on-virtualbox>`_. it's really easy to install and works great and this guide will be step by step so you can follow along.

This is not a GIT setup guide, if you want to properly fork and pull from the GIT repository follow this guide `Contribute to someone's repository <http://kbroman.org/github_tutorial/pages/fork.html>`_.

1. First follow the steps 1 - 4 in the pillowncase :ref:`install_ubuntu` guide, this will set up a Python 3.5 virtual environment and be ready to go.  Stop before the part where you install pillowncase using pip.

2. Install python packages required by the development environment, there are 4 packages (pillowncase only required pillow and cryptography to run but the others are needed for testing and documentation)

	- `pillow <https://python-pillow.org/>`_.
		Extension of the PIL Image library.

	- `cryptography <https://cryptography.io>`_.
		Provides tools to encrypt the hidden data if required.

	- `nose <http://nose.readthedocs.io>`_.
		Test tools to allow easy testing

	- `sphinx <http://www.sphinx-doc.org>`_.
		Documentation support

	With the virtual environment running from step 1. install the above using pip

	::

		(.env) mark@computer:pillowncase$ pip install pillow cryptography nose sphinx


3. Get the development files from github.

	Either browse to `pillowncase <https://github.com/ArchageXIII/pillowncase>`_. and select download zip and download to the pillowncase folder you created or from the command line.

	::

		(.env) mark@computer:pillowncase$ wget "https://github.com/ArchageXIII/pillowncase/archive/master.zip"

	Then either unzip in the pillowncase folder from the GUI or via command line and copy the files and folders to the current directory

	::

		(.env) mark@computer:pillowncase$ unzip master.zip
		(.env) mark@computer:pillowncase$ rsync -ua pillowncase-master/ .
		(.env) mark@computer:pillowncase$ rm -r pillowncase-master/
		(.env) mark@computer:pillowncase$ rm master.zip
		(.env) mark@computer:pillowncase$ ls -lart
		drwxrwxr-x 2 mark mark  4096 Dec 31 21:32 tests
		-rw-rw-r-- 1 mark mark  1398 Dec 31 21:32 setup.py
		-rw-rw-r-- 1 mark mark  1500 Dec 31 21:32 README.md
		drwxrwxr-x 3 mark mark  4096 Dec 31 21:32 pillowncase
		-rw-rw-r-- 1 mark mark    37 Dec 31 21:32 MANIFEST.in
		-rw-rw-r-- 1 mark mark 35141 Dec 31 21:32 LICENSE
		-rw-rw-r-- 1 mark mark  1067 Dec 31 21:32 .gitignore
		drwxrwxr-x 2 mark mark  4096 Dec 31 21:32 docs
		drwxrwxr-x 2 mark mark  4096 Dec 31 21:32 dist
		drwxrwxr-x 3 mark mark  4096 Jan  1 16:37 ..
		drwxrwxr-x 6 mark mark  4096 Jan  1 17:29 .env
		drwxrwxr-x 8 mark mark  4096 Jan  1 17:32 .

4. Install pillowncase in development mode, this will let you see instant changes to any code but it will run as if it's an installed package.

	::

		(.env) mark@computer:pillowncase$ python setup.py develop

	If you ever need to uninstall it in the virtual environment it's like this.

	::

		(.env) mark@computer:pillowncase$ python setup.py develop --uninstall

5. Now you should be able to run the test suite and make sure you have no errors, the full tests are quite involved (and the code it a bit slow at the moment!) so it will take a while (~424 secs) the test scripts clean up after them selfs, if any fail the file they were reading or writing will be somewhere in tmp_tests.

	::

		(.env) mark@computer:pillowncase$ nosetests -v

6. Build install file, this will create a versioned gzip file in dist/pillowncase-0.2.tar.gz you can test installing this in other environments (not this one) using pip e.g. `pip install ../pillowncase/dist/pillowncase-0.2.tar.gz`

	::

		(.env) mark@computer:pillowncase$ python setup.py sdist


7. The documentation should auto build, to test and make sure no errors do the following, first clear out any thing that was there then remake all documentation, it will write the output to docs/_build/html

	::

		(.env) mark@computer:pillowncase$ cd docs
		(.env) mark@computer:pillowncase\docs$ make clean
		(.env) mark@computer:pillowncase\docs$ make html

8. Review the documentation on how to use the :doc:`pillowncase` and what is included.

9. Folder setup and files of note

	- docs/
		documents created by sphinx and and manual documentation pages, configured only to include functions that have doc strings and will automatically take the version number from the installed pillowncase package.
	
	- docs/conf.py
		sphinx setup file you need to update release number here to match setup.py

	- docs/index.rst
		root index file that the docs get built off.
	
	- tests/
		test scripts and supporting files, see `nose <http://nose.readthedocs.io>`_. documentation on how it works, will by default run any file (and function in that file) that starts with test\_ 

	- tmp_tests/
		automatically created if not there when nosetests runs, some tests create and check random data to make sure it comes out as it went in, if one of those random tests fails the file will still be there and details captured so you can recreate and bug fix.

	- pillowncase/files/
		static files included in the package for default behavior (and to give some default images to hide in)

	- .gitignore
		files not to include in versioning

	- MANIFEST.in
		additional non python files to include in distribution package

	- setup,py
		config file for distribution build main method is aliased to pNcase here
		
		'entry_points': {'console_scripts': ['pNcase = pillowncase.\_\_main__:main']}

	- requirements.txt
		a pip requirements file that read the docs needs to install this package virtual to auto create this documentation linked to git repository.

	- pillowncase.egg-info/PKG-INFO
		created after build has run this is the file you would upload to pypi if you were registering your own package.

------------------------------------------
Notes to self and useful links
------------------------------------------

In no particular order...

Great resource for getting loads of test UTF-8 codes.

	`<https://github.com/bits/UTF-8-Unicode-Test-Documents>`_.

General GIT commands (after initial creation of a repository on GIT website)

	Initial setup

	::

		sudo apt-get install git
		git config --global user.name "Username"
		git config --global user.email "username@email.com"
		mkdir pillowncase
		git init pillowncase/
		cd pillowncase
		git remote add origin https://github.com/Username/pillowncase
		git pull origin master

		General usage in not order just notes

	::

		git commit -m "some_message"    -- commit changes
		git push -u origin master       -- upload working repository
		git add filename                --
		add <folder>/*                  -- general commands for adding new files etc. to be versioned
		git add *                       --
		git add --all folder/           --
		git status                      -- get the current status of whats been changed etc.
		git branch -a                   -- what branches do I have and which one am I in
		git checkout -b develop         -- create new branch
		git push -u origin develop      -- push that branch back to GIT website
		git clone <url>                 -- clone a git repository will defeult to master active branch
		git merge develop               -- if i'm in master and want to bring in my dev environment
		git pull origin master          -- if i just want to brin my develop environment to reflect master
		git merge master                -- if i'm in master and want to bring in my dev environment

	Branching and merging, sensible description for low change small team

	`<https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging>`_.

	How to fork other peoples repositories

	`<http://kbroman.org/github_tutorial/pages/fork.html>`_.

	Resolving conflicts

	`<https://githowto.com/resolving_conflicts>`_.

General Sphinx / RST info

	`<http://www.sphinx-doc.org/en/1.5.1/markup/inline.html>`_.

	`<http://docutils.sourceforge.net/docs/ref/rst/directives.html>`_.

	Auto setup core set of documents for a package

	::

		sphinx-apidoc -F -o docs pillowncase

General Links

	Sensible guide on getting all this together to publish on pypi

	`<https://tom-christie.github.io/articles/pypi/>`_.
