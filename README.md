# pillowncase
I had some spare time over xmas and wanted to learn python in a bit more detail to the point of making something I could distribute, this is what I came up with, enjoy!

Hide any data in an image
While I get proper instructions up if you want to play
(depends on pillow and cryptography should download automaticaly)
if you are on ubuntu and cryptography does not install assuming you are running python 3.5
sudo apt-get install build-essential libssl-dev libffi-dev python3.dev

then install using pip (pip install cryptography), I'd suggest in a virtual environment will document that later in the build environment setup.  Windows 10 it should just install with no extra fiddling.


pip install pillowncase

to run if you want a quick play.

python -m pillowncase
this will create a test image with a file embedded 

to extract the file
python -m pillowncase -a decode -i pNcase_small_test.png

you will get a text file out called pNcase_test.txt

python -m pillowncase -h to get an idea of other options

while I get proper documentation written up have a look through the tests directory to get some idea of ways to use it and options.

if you want to run the test suite, pull the project from git
make sure you have nose installed (pip install nose) as well as pillow and cryptography.

then run nosetests -v from the root of the package directory it will run through everything (and take some time)

it's a bit slow at the moment as it's iterating over every pixel I need to get my head around numpy and do it with that I think but it's fine as a working proof of concept now! 

# How to set up build environment and usage instructions
coming soon!
