import argparse
try:
	from pillowncase import pncase
except Exception:
	import pncase
import sys
import os

parser = argparse.ArgumentParser(description='A utility to hide any file type in an image file and retreive it NOTE: decoded files are saved in the directory you run this so be careful if you don\'t know what you are decoding')
parser.add_argument("-f", "--input_file", type=str, help="File to hide in image, if not supplied test data is used and a test image created", default="small_test")
parser.add_argument("-i", "--image_file", type=str, help="Optional image file to hide input file in, if not there for encode a square data image is created with daw image data", default="")
parser.add_argument("-o", "--output_file", type=str, help="Optional output file name for created image (.png only) if not specified pNcase_(input_file).png used")
parser.add_argument("-c", "--channels", type=str, help="Optional channel letter(s) to store data in (RGBA) alpha will be added for output if not present and specified default (%(default)s)", default='RGB')
parser.add_argument("-g", dest="granularity", help="Optional -g fine (larger file) -gggggggg replace picture (smaller file) default (-gggg) unless creating only data image when its (-gggggggg) by default",action="count")
parser.add_argument("-a", "--action", type=str, help="encode or decode, default encode, decode with no image file will error and exit", default="encode")
parser.add_argument("-v", "--verbose", help="Enable verbose output when running supports multiple -vvv beware adding too many!",action="count",default=0)
parser.add_argument("-m", "--magic_header", type=str, help="Magic headder that pNcase looks for to start decoding defaults to XYZZY if you change it you'll need to remember what it was to decode or be good reading binary, beware!", default="XYZZY")
parser.add_argument("-j", "--custom_channels", type=str, help="Overides granularity specify RGBA bit distribution manualy 0 means no bits in that channel e.g. 1240  means R=1, G=2, B=4, A=0", default="")
parser.add_argument("--do_not_resize_image", dest='resize_image', help="By default this will resize any image provided image to hide in to match data to be hidden, if you only have a small amount of data to hide you might not want to resize, use -g in this case to hide it well", action='store_false')
parser.set_defaults(resize_image=True)
parser.add_argument("--encrypt_data", dest='encrypt_data', help="Encrypt to make it hard to guess if there is a file embedded or "
																	 "not (it's not hard to guess, without encryption you could read the first 3 RGB Image pix to get the bit distribution then try "
																	 " and read the rest of the image looking for the byte separators that I used in the header.)"
																	 "  This makes it harder, to aid conveniance so you dont have to pass data length as well as a key I include "
																	 "the data length XOR'd with the first 5 bytes of the same key. This makes it is vunrable to brute force to reverse the first 5 bytes of the key as I've used it to XOR "
																	 "the lead in and data length as well, thats still a lot of data to crunch (if there is anything in the image at all)  "
																	 " Esentialy you get every XOR'd combination of leadin bits that have no values over 8 then for each on then see if you can find an XOR concatonating"
																	 " the next 5 bytes up as padded 8 bit binary and converting to an int comes to a value thats less then the total image size. you'll probably"
																	 "have a few combinations that match that but it will reduce the number of guesses on the first 5 bytes of the 32 byte key"
																	 " After that you'll still have to gues the rest of the key which is not trivial but slightly less hard work than getting all of it."
																	 "Saying that don't forget, you can read and hide any binary file using this code so just encrypt your "
																	 "file with stronger encryption before hiding if you want to and are feeling particulary paranoid!", action='store_true')
parser.set_defaults(encrypt_data=False)
parser.add_argument("-k", "--key", type=str, help="Required to decrypt header, optional for encrypting, one will get generated if you don't supply one when encrypting, you can then reuse if you want to use the same key to encrypt multiple files", default="")


args = parser.parse_args()
#setting a default value on count adds to default value when one added.
if not args.granularity:
	if len(args.image_file) == 0:
		args.granularity = 8
	else:
		args.granularity = 4

#check case etc.

if not args.output_file:
	if args.action == "encode":
		head, tail = os.path.split(args.input_file)
		args.output_file = "pNcase_" + tail + ".png"
	elif args.action == "decode":
		args.output_file =""

if args.action == "decode" and len(args.image_file) == 0:
	print("You need to provide an image to decode, type -h for help")
	sys.exit(1)
try:
	pnc = pncase.ManipulateImage(channels=args.channels,
							     granularity=args.granularity,
							     magic_header=args.magic_header,
							     verbose=args.verbose,
							     custom_channels=args.custom_channels,
							     key=args.key,
							     encrypt_data=args.encrypt_data)
except ValueError as err:
	print (err)
	print ("Exiting")
	sys.exit(2)
if args.action == "encode":
	
	try:
		pnc.encode(input_file=args.input_file,
				   image_file=args.image_file,
				   output_file=args.output_file,
				   resize_image=args.resize_image,
				   key=args.key)
	except IOError as err:
		print (err)
		print ("Exiting")
		sys.exit(2)
elif args.action == "decode":
	try:
		pnc.decode(image_file=args.image_file,
				   key=args.key,
				   output_file=args.output_file)
	except IOError as err:
		print (err)
		print ("Exiting")
		sys.exit(2)
else:
	Print("-a is either encode or decode (defaults to encode)")
