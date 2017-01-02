import argparse
try:
	from pillowncase import pncase
except Exception:
	import pncase
import sys
import os

def main():
	"""you can run pillowncase from the command line where it invokes this main function you can run it as `pNcase` but for convenience it is aliased to pNcase when installed.

	Example::

		$ pNcase
		::encode::
		::Reading Datafile: pillowncase/pillowncase/files/pNcase_test.txt
		::Resizing Image to fit to data
		::Writing data to Image
		::Progress: 100%
		::Image 'pNcase_small_test.png' created and saved

		$ pNcase -a decode -i pNcase_small_test.png
		::Decode::
		::Opened Image-file: pNcase_small_test.png
		::Reading data from Image
		::Progress: 100%::Found hidden file: pNcase_test.txt
		::Successfully read data
		::All done Data Written to file: pNcase_test.txt

	
	-h, --help  Show help message text
	-f, --input_file filename  File to hide in image, if not supplied test data is used and a test image created
	-i, --image_file filename  Image file to hide input file in, if not there for encode a square data image is created with raw image data
	-o, --output_file filename  Output file name for created image (.png only) if not specified pNcase_(input_file).png used
	-c, --channels rgba  default 'RGB' channel letter(s) to store data in (RGBA) alpha will be added for output if not present and specified 
	-g gggggggg  Fine -g (larger file) -gggggggg (smaller file) default (-gggg) unless creating only data image when its (-gggggggg)
	-a, --action selection  'encode' or 'decode', default encode, decode with no image file will error and exit
	-v, --verbose vvvvvvvv  default v basic output, the more v's the more output
	-m, --magic_header header  Magic header that pNcase looks for to start decoding defaults to XYZZY if you change it you'll
					need to remember what it was to decode or be good reading binary, beware!
	-j, --custom_channels channels  Overrides granularity specify RGBA bit distribution manually 0 means no bits in that channel e.g. 1240  means R=1, G=2, B=4, A=0
	--do_not_resize_image  By default this will resize any image provided image to hide in to match data to be hidden,
					if you only have a small amount of data to hide you might not want to resize, use -g in this case to hide it well
	--encrypt_data  default False, change to True if you want to encrypt the lead in header and data, uses a
		 			combination of XOR and Fernet, do some research look at the code see if that meets your needs, you will need the key to decrypt,
		 			a key is auto generated if not supplied.  Don't forget you can encrypt your data to hide however you like outside of
		 			this code, it will just do a like for like binary read and store of whatever file you point it at.
	-k, --key key  Required to decrypt header, optional for encrypting, one will get generated if you don't supply one when encrypting,
					you can then reuse if you want to use the same key to encrypt multiple files

	Other Examples

		Encrypt and Decrypt::

			$ pNcase -i kitten -f medium_test -j 2240 --encrypt_data
			::encode::
			::Reading Datafile: pillowncase/pillowncase/files/pg29809.txt
			::Encrypting Data
			::Resizing Image to fit to data
			::Writing data to Image
			::Progress: 100%
			::Image 'pNcase_medium_test.png' created and saved

			***KEEP THIS KEY SAFE YOU CANT DECRYPT WITHOUT IT***

			***if your key starts with a - and you are using the example main class explicitly
				reference it in the command line with -k='-your key starting with a -'***

			::
			::Decrypt Key: PaNmvZ4y3pmOcdDlHak0c393XR5FpIn2SKfZZ0WA52o=
			::

			$ pNcase -i pNcase_medium_test.png -k PaNmvZ4y3pmOcdDlHak0c393XR5FpIn2SKfZZ0WA52o= -a decode
			::Decode::
			::Opened Image-file: pNcase_medium_test.png
			::Reading data from Image
			::Progress: 100%
			::Decrypting Data
			::Using Key: PaNmvZ4y3pmOcdDlHak0c393XR5FpIn2SKfZZ0WA52o=
			::Found hidden file: pg29809.txt
			::Successfully read data
			::All done Data Written to file: pg29809.txt

		Create raw data image::

			$ pNcase -f medium_raw_test
			::encode::
			::Reading Datafile: pillowncase/pillowncase/files/pg29809.txt
			::Creating Image to put data in
			::Writing data to Image
			::Progress: 100%
			::Image 'pNcase_medium_raw_test.png' created and saved

			$ pNcase -a decode -i pNcase_medium_raw_test.png
			::Decode::
			::Opened Image-file: pNcase_medium_raw_test.png
			::Reading data from Image
			::Progress: 100%::Found hidden file: pg29809.txt
			::Successfully read data
			::All done Data Written to file: pg29809.txt




	"""
	parser = argparse.ArgumentParser(description='A utility to hide any file type in an image file and retrieve it NOTE: decoded files are saved in the directory you run this so be careful if you don\'t know what you are decoding')
	parser.add_argument("-f", "--input_file", type=str, help="File to hide in image, if not supplied test data is used and a test image created", default="small_test")
	parser.add_argument("-i", "--image_file", type=str, help="Optional image file to hide input file in, if not there for encode a square data image is created with daw image data", default="")
	parser.add_argument("-o", "--output_file", type=str, help="Optional output file name for created image (.png only) if not specified pNcase_(input_file).png used")
	parser.add_argument("-c", "--channels", type=str, help="Optional channel letter(s) to store data in (RGBA) alpha will be added for output if not present and specified default (%(default)s)", default='RGB')
	parser.add_argument("-g", dest="granularity", help="Optional -g fine (larger file) -gggggggg replace picture (smaller file) default (-gggg) unless creating only data image when its (-gggggggg) by default",action="count")
	parser.add_argument("-a", "--action", type=str, help="encode or decode, default encode, decode with no image file will error and exit", default="encode")
	parser.add_argument("-v", "--verbose", help="Enable verbose output when running supports multiple -vvv beware adding too many!",action="count",default=1)
	parser.add_argument("-m", "--magic_header", type=str, help="Magic header that pNcase looks for to start decoding defaults to XYZZY if you change it you'll need to remember what it was to decode or be good reading binary, beware!", default="XYZZY")
	parser.add_argument("-j", "--custom_channels", type=str, help="Overrides granularity specify RGBA bit distribution manually 0 means no bits in that channel e.g. 1240  means R=1, G=2, B=4, A=0", default="")
	parser.add_argument("--do_not_resize_image", dest='resize_image', help="By default this will resize any image provided image to hide in to match data to be hidden, if you only have a small amount of data to hide you might not want to resize, use -g in this case to hide it well", action='store_false')
	parser.set_defaults(resize_image=True)
	parser.add_argument("--encrypt_data", dest='encrypt_data', help="default False, change to True if you want to encrypt the lead in header and data, uses a"
		 															"combination of XOR and Fernet, do some research look at the code see if that meets your needs, you will need the key to decrypt,"
		 															"a key is auto generated if not supplied.  Don't forget you can encrypt your data to hide however you like outside of"
		 															"this code, it will just do a like for like binary read and store of whatever file you point it at.", action='store_true')
	parser.set_defaults(encrypt_data=False)
	parser.add_argument("-k", "--key", type=str, help="Required to decrypt header, optional for encrypting, one will get generated if you don't supply one when encrypting, you can then reuse if you want to use the same key to encrypt multiple files", default="")


	args = parser.parse_args()
	#setting a default value on count adds to default value when one added.
	if not args.granularity:

		if len(args.image_file) == 0:
			if args.input_file.upper() not in ['SMALL_TEST','MEDIUM_TEST','LARGE_TEST']:
				args.granularity = 8
			else:
				args.granularity = 4
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
		print("You need to provide an image to decode (-i image_file), type -h for help")
		sys.exit()

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
		sys.exit()
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
			sys.exit()
	elif args.action == "decode":
		try:
			pnc.decode(image_file=args.image_file,
					   key=args.key,
					   output_file=args.output_file)
		except IOError as err:
			print (err)
			print ("Exiting")
	else:
		Print("-a is either encode or decode (defaults to encode)")

if __name__ == "__main__":
	main()