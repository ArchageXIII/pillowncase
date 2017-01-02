try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': ('Store and retreive any file data in any image'),
    'author': 'Mark Edwards',
    'url': 'https://github.com/ArchageXIII/pillowncase',
    'download_url': 'https://github.com/ArchageXIII/pillowncase',
    'author_email': 'mark.3dwards@gmail.com',
    'version': '0.3',
    'licence': 'GNU GPL',
    'install_requires': ['cryptography','pillow'],
    'packages': ['pillowncase'],
    'package_data':{'pillowncase':['files/*']},
    'name': 'pillowncase',
    'platforms':['windows','linux'],
    'long_description':""" 
        Takes and file type and breaks it into small chunks hiding it in the low end bits of the image
        You can specify what chanels including alpha and how many bits you want to hide in each channel

        Full documentation on the github site
        """,
    'clasifiers':[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: GNU General Public License (GPL)',
        'Operating System :: Windows :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Desktop Environment',
        'Topic :: Image Processing :: Obfuscation'
                 ],
    'entry_points': {'console_scripts': ['pNcase = pillowncase.__main__:main']},
    'zip_safe': False
}

setup(**config)
