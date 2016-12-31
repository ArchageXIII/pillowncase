from PIL import Image
import math
import os
from cryptography.fernet import Fernet
import random
import sys
import base64


class ManipulateImage:
	"""Store any file in any image as a png file.
	
	:param str channels: takes any combination of RGBA this defines what channels you want to store the file data in, 
		if the source image does not have an alpha channel (A) one is created.
	:param int granularity: a value between 1 and 8, 1 is fine (large file size but little visual 
		difference to original image) 8 is complete replacement with the data to be hidden.
	:param str magic_header: header used internal to see where the data starts, in most cases you wont ever need to change this.
		if you do change it you will have to supply it to decode.  See decode function.
	:param int verbose: set to 1 for general command line usage and feedback, higher for debugging leave at default 0
		which is no sys out for class usage unless you are having issues.
	:param str custom_channels: overrides the channels parameter here you can specify exactly what bit distribution
		you want in the image expects text string in the format 1111 e.g. 2034 means 2 px in R, none in G, 3 in B and 4 in A
	:param bool encrypt_data: default False, change to True if you want to encrypt the lead in header and data, uses a
		 combination of XOR and Fernet, do some research look at the code see if that meets your needs, you will need the key to decrypt,
		 a key is auto generated if not supplied.  Don't forget you can encrypt your data to hide however you like outside of
		 this code, it will just do a like for like binary read and store of whatever file you point it at.
	:param str key: if you have a key and want to encrypt using it put it here as a string e.g. you want to encode a lot of
		images with the same key, if it's left blank one will get generated if encrypt_data=True.
		See :py:func:`~ManipulateImage.decode` for an example using encryption.
	:raises ValueError: If input values provided are out of range
	
	Example usage::

		>>> from pillowncase import pncase
		>>> pnc = pncase.ManipulateImage(verbose=1)
		>>> pnc.encode()
		::encode::
		::Reading Datafile: pillowncase/pillowncase/files/pNcase_test.txt
		::Resizing Image to fit to data
		::Writing data to Image
		::Progress: 100%
		::Image 'pNcase.png'' created and saved
		>>> pnc.decode(image_file='pNcase.png')
		::Decode::
		::Opened Image-file: pNcase.png
		::Reading data from Image
		::Progress: 100%
		::Found hidden file: pNcase_test.txt
		::Successfully read data
		::All done Data Written to file: pNcase_test.txt
	"""
	

	def __init__(self,channels="RGB",granularity=4,magic_header="XYZZY",verbose=0,custom_channels='',encrypt_data=False, key=''):
		#set up common vars that will be used in the class
		self.verbose = verbose

		self._start = 0x02
		self._end = 0x03
		self._r = 0
		self._g = 1
		self._b = 2
		self._a = 3
		self.magic_header = magic_header

		#for RGBA max value is 8, 0 means don't write to this channel
		#default all to 0 order is RGBA
		self.chan = [0]*4

		#if we have custom channel map use that else use granularity
		if len(custom_channels)>0:
			if len(custom_channels) != 4:
				raise ValueError("ERROR - Expecting custom channel numeric string of 4, got {0} order is read as RGBA e.g. 4440".format(custom_channels))
			try:
				self.chan[self._r] = int(custom_channels[0])
				if self.chan[self._r] > 8:
					raise ValueError("ERROR - individual custom channel value cannot be greater than 8")
				self.chan[self._g] = int(custom_channels[1])
				if self.chan[self._g] > 8:
					raise ValueError("ERROR - individual custom channel value cannot be greater than 8")
				self.chan[self._b] = int(custom_channels[2])
				if self.chan[self._b] > 8:
					raise ValueError("ERROR - individual custom channel value cannot be greater than 8")
				self.chan[self._a] = int(custom_channels[3])
				if self.chan[self._a] > 8:
					raise ValueError("ERROR - individual custom channel value cannot be greater than 8")
				if sum(self.chan) == 0:
					raise ValueError("ERROR - All Channels cannot be 0")
			except Exception as err:
				raise ValueError("ERROR - unable to parse custom channel '{0}' see below for additional information".format(custom_channels),err )

		else:
			#check we have no more than 8 bits no less than 1
			if granularity > 8:
				granularity = 8
			elif granularity <= 0:
				granularity = 1

			#parse channel input
			for i, c in enumerate(channels.upper()):
				if c == 'R':
					self.chan[self._r] = granularity
				elif c == 'G':
					self.chan[self._g] = granularity
				elif c == 'B':
					self.chan[self._b] = granularity
				elif c == 'A':
					self.chan[self._a] = granularity

		self.encrypt_data = encrypt_data

		if len(key) > 0:
			self.encrypt_data = True

		#if encrypt and there is no key then generate one
		if self.encrypt_data:
			if len(key) == 0:
				self.key = Fernet.generate_key()
			else:
				self.key = str.encode(key,'utf-8')
		else:
			self.key = str.encode("not encrypted",'utf-8')
			self.encrypt_data = False

		if self.verbose >= 2:
			print ("::ManipulateImage:__init__::")
			print ("  Channels:", channels)
			print ("  Granularity:", granularity)
			print ("  Magic Header:", magic_header)
			print ("  Encrypt Header key:", self.key.decode('utf-8'))
			print ("  Verbose:", verbose)



		if sum(self.chan) <1:
			raise ValueError("ERROR - No valid channels provided, you provided '{0}' should be at least 1 channel from 'RGBA'".format(channels)) 

		if (self.chan[self._a]) > 0:
			self.output_image_type = "RGBA"
		else:
			self.output_image_type = "RGB"
		#number of bits per pix
		self.number_of_bits = sum(self.chan)

		if self.verbose >= 2:
			print("  Channels successfully created bits to be stored pre channel (R, G, B, A):",self.chan)
			print("  Total Bits to store in each Px:",self.number_of_bits)
			print("  Image type required to support channels:", self.output_image_type)


	def xor(self, data,key):

		o = bytearray()
		l = len(key)
		kl = 0

		for i,d in enumerate(data):
			o.append(d^key[kl])
			kl += 1
			if kl >= l:
				kl = 0

		return o

	def enc_dec_header(self,l):

		if (len(self.key) < 2):
			raise IOError("Key length needs to be at least 2")
		elead_in_string = bytearray()
		elead_in_string.append(int(l[0:8],2))
		elead_in_string.append(int(l[8:16],2))

		ekey = bytearray()
		ekey.append(self.key[0])
		ekey.append(self.key[1])

		elead_in_string = self.xor(elead_in_string,ekey)

		return bin(elead_in_string[0])[2:].zfill(8) + bin(elead_in_string[1])[2:].zfill(8)

	def get_key(self):
		"""Gets the encryption key if there is one.

		:return: the encryption key as a decoded UTF-8 string
		 if no key is set it will return a string containing *"not encrypted"*
		:rtype: str


		 Example usage::

		 	>>> from pillowncase import pncase
			>>> pnc = pncase.ManipulateImage(verbose=1,encrypt_data=True)
			>>> pnc.encode()
			::encode::
			::Reading Datafile: pillowncase/pillowncase/files/pNcase_test.txt
			::Encrypting Data
			::Resizing Image to fit to data
			::Writing data to Image
			::Progress: 100%
			::Image 'pNcase.png'' created and saved
			
			***KEEP THIS KEY SAFE YOU CANT DECRYPT WITHOUT IT***
			
			***if your key starts with a - and you are using the example main class explicitly 
				reference it in the command line with -k='-your key starting with a -'***
			
			::
			::Decrypt Key: VVXeB8qWM1YYiQSud2vE0o0JZqRzwNUFjcBCGjI5rhs=
			::
			>>> print (pnc.get_key())
			VVXeB8qWM1YYiQSud2vE0o0JZqRzwNUFjcBCGjI5rhs=
		"""
		return self.key.decode('utf-8')

	def set_key(self,key):
		"""Sets the encryption key to a specific string, note the key must be compatible with Fernet
		if you are not sure, let the initial encode process generate a key for you on first run
		and use that going forward if you want to encrypt a lot of files with the same key.
		This will not raise an error until the key is used by decode() or encode()

		:param str key: the encryption key.

		Example usage::

			>>> from pillowncase import pncase
			>>> pnc = pncase.ManipulateImage(verbose=1)
			>>> pnc.set_key('VVXeB8qWM1YYiQSud2vE0o0JZqRzwNUFjcBCGjI5rhs=')
			>>> pnc.encode(image_file='small_test')
			::encode::
			::Reading Datafile: pillowncase/pillowncase/files/pNcase_test.txt
			::Encrypting Data
			::Resizing Image to fit to data
			::Writing data to Image
			::Progress: 100%
			::Image 'pNcase.png'' created and saved
			
			***KEEP THIS KEY SAFE YOU CANT DECRYPT WITHOUT IT***
			
			***if your key starts with a - and you are using the example main class explicitly 
				reference it in the command line with -k='-your key starting with a -'***
			
			::
			::Decrypt Key: VVXeB8qWM1YYiQSud2vE0o0JZqRzwNUFjcBCGjI5rhs=
			::
		"""
		self.key = str.encode(key,'utf-8')
		self.encrypt_data = True
	
	def get_output_file(self):
		"""Gets the created output file as a string
		
		:return: output file name
		:rtype: str

		Example usage::

			>>> from pillowncase import pncase
			>>> pnc = pncase.ManipulateImage()
			>>> pnc.encode(image_file='small_test')
			>>> print (pnc.get_output_file())
			pNcase.png
		"""
		return self.output_file

	def get_input_file(self):
		"""Gets the data input file as a string

		:return: input file name
		:rtype: str

		Example usage::

			>>> from pillowncase import pncase
			>>> pnc = pncase.ManipulateImage()
			>>> pnc.encode(image_file='small_test')
			>>> print (pnc.get_input_file())
			pillowncase/pillowncase/files/pNcase_test.txt
		"""
		return self.input_file

	def get_data_output_file(self):
		"""Gets the created hidden data file as a string

		:return: extracted hidden data file name
		:rtype: str


		Example usage::

			>>> from pillowncase import pncase
			>>> pnc = pncase.ManipulateImage(verbose=1)
			>>> pnc.encode(image_file='small_test')
			::encode::
			::Reading Datafile: pillowncase/pillowncase/files/pNcase_test.txt
			::Resizing Image to fit to data
			::Writing data to Image
			::Progress: 100%
			::Image 'pNcase.png'' created and saved
			>>> pnc.decode(image_file='pNcase.png')
			::Decode::
			::Opened Image-file: pNcase.png
			::Reading data from Image
			::Progress: 100%  Found File Name: pNcase_test.txt
			::Found hidden file: pNcase_test.txt
			::Successfully read data
			::All done Data Written to file: pNcase_test.txt
			>>> print (pnc.get_data_output_file())
			pNcase_test.txt
		"""
		return self.data_output_file

	def get_magic_header(self):
		"""Gets the magic header as a string

		:return: magic header
		:rtype: str


		Example usage::

			>>> from pillowncase import pncase
			>>> pnc = pncase.ManipulateImage()
			>>> print (pnc.get_magic_header())
			XYZZY
		"""
		return self.magic_header

	def replacebits(self,bits,replace):
		bitshift = len(replace)
		if bits > 255 or bits < 0:
			raise ValueError("ERROR - Bits must be in the range 0 - 255")
		elif bitshift > 8:
			raise ValueError("ERROR - replace must be a string no longer than 8")
		#if theres an empty string just return what was passed with no masking.
		if len(replace) == 0:
			mask = 255
			result = bits
		else:
			#clear low end bits to length of string
			#cant use and maske easily as need to account for single 0 getting passed
			mask = bits >> bitshift
			mask = mask << bitshift
			#now we know we only have 0's we can or it
			#add in new bits
			#change replace string to int version of bin string
			result = mask | int(replace,2)
		if self.verbose >=3:
			print("Masking bits, bits, mask, replace, result", bin(bits)[2:].zfill(8),
															   bin(mask)[2:].zfill(8),
															   replace.zfill(8),
															   bin(result)[2:].zfill(8))
		return result


	def encode(self,input_file="small_test",image_file="",output_file="pNcase.png",resize_image=True,key=''):
		"""Store any file in any image as a png file.

		:param str input_file: a string with the path to the file you want to hide, there are 4 test scenarios included.

			All examples are royalty free and include licenses as required passing one of the strings below will create
			example image files of varying sizes.

			Example::

				input_file='small_test'
				input_file='medium_test'
				nput_file='medium_raw_test'
				input_file='large_test'
				

		:param str image_file: a string containing the path to the image file you would like to hide the file in, if no file is passed an empty square image is produced
			and just the data is written, this is the most optimal way to store the data but it is not hidden (but looks cool), there are 5 images included as defaults 
			if you want to use them instead of your own images.

			All included images are created and owned by me and released under the same licensing as this project.

			Example::

				image_file='FLOWERS'
				image_file='HORSE'
				image_file='PNCASE'
				image_file='KITTEN'
				image_file='KATIE'

		:param str output_file: the output image file name, will always be png, if none is passed it defaults to pNcase.png this is the image file with the data hidden in it.
		:param bool resize_image: by default is an image is supplied it will be resized up or down to the optimum size to fit the data, if you only have
			a small amount of data to hide sometimes it will be better to keep the image at it's initial size.  If the data would then exceed this size
			an error will be thrown.
		:param str key: if you have a key and want to encrypt using it put it here as a string e.g. you want to encode a lot of
			images with the same key, if it's left blank and you did not set *encrypt_data=True* in the class initiator it will
			not be encrypted.
		:raises IOError: if it can't read or write any of the files successfully.
		
		Example usage see :py:func:`~ManipulateImage.decode` for an example using encryption::

			>>> from pillowncase import pncase
			>>> pnc = pncase.ManipulateImage(verbose=1,granularity=2)
			>>> pnc.encode(image_file='KATIE',input_file='medium_test',output_file='katie_test.png')
			::encode::
			::Reading Datafile: pillowncase/pillowncase/files/pg29809.txt
			::Resizing Image to fit to data
			::Writing data to Image
			::Progress: 100%
			::Image 'katie_test.png'' created and saved
			>>> pnc.decode(image_file='katie_test.png')
			::Decode::
			::Opened Image-file: katie_test.png
			::Reading data from Image
			::Progress: 100%  Found File Name: pg29809.txt
			::Found hidden file: pg29809.txt
			::Successfully read data
			::All done Data Written to file: pg29809.txt
		"""


		if self.verbose >= 1:
			print ("::encode::")

		if output_file.upper()[-4:] != ".PNG":
			output_file += ".png"
			if self.verbose >= 2:
				print("Output file has to end in .PNG, added .PNG for file path")

		self.output_file = output_file

		resource_path = os.path.join(os.path.dirname(__file__),"files")
		
		#preloaded images
		if image_file.upper() == "FLOWERS":
			image_file = os.path.join(resource_path, "flowers.jpg")
		elif image_file.upper() == "HORSE":
			image_file = os.path.join(resource_path, "horse.jpg")
		elif image_file.upper() == "PNCASE":
			image_file = os.path.join(resource_path, "pNcase.png")
		elif image_file.upper() == "KITTEN":
			image_file = os.path.join(resource_path, "kitten.jpg")
		elif image_file.upper() == "KATIE":
			image_file = os.path.join(resource_path, "katie.jpg")

		if input_file.upper() == "SMALL_TEST":
			input_file = os.path.join(resource_path, "pNcase_test.txt")
			if len(image_file) == 0:
				image_file = os.path.join(resource_path, "pNcase.png")


		elif input_file.upper() == "MEDIUM_TEST":
			input_file = os.path.join(resource_path, "pg29809.txt")
			if len(image_file) == 0:
				image_file = os.path.join(resource_path, "horse.jpg")


		elif input_file.upper() == "LARGE_TEST":
			input_file = os.path.join(resource_path, "bitshift.zip")
			if len(image_file) == 0:
				image_file = os.path.join(resource_path, "flowers.jpg")

		elif input_file.upper() == "MEDIUM_RAW_TEST":
			input_file = os.path.join(resource_path, "pg29809.txt")


		if self.encrypt_data:
			if len(key) >0:
			#the encode method has passed an ove ride key use that
				self.key = str.encode(key,'utf-8')

		self.input_file = input_file

		if self.verbose >= 2:
			print ("  Input file:", input_file)
			print ("  Image File:", image_file)
			print ("  Output File:", output_file)
			print ("  Key:", self.key.decode('utf-8'))
			print ("  Encrypt Data:", self.encrypt_data)

		#always start with byte distribution these will be 
		#spread over the first 16 bytes 1 bit per byte (if they are there at all 1111 1111 1111 1111)

		#Add header can be any length just needs to match
		data_out = bytearray()
		data_out.extend(str.encode(self.magic_header,'utf-8'))
		
		head, tail = os.path.split(input_file)

		#encode the file name to bytes utf-8
		data_out.append(self._start)
		data_out.extend(str.encode(tail,'utf-8'))
		data_out.append(self._end)

		if self.verbose >= 1:
			print("::Reading Datafile:", input_file)
		#read data file that needs to be hidden as binary
		try:
			with open(input_file, "rb") as binary_file:
				file_data = binary_file.read()
		except IOError as err:
			raise IOError("ERROR - Unable to open file to be hidden ('{0}') check path and try again{1}".format(input_file,err))

		#add size of file
		data_out.append(self._start)
		data_out.extend(str.encode(str(len(file_data))))
		data_out.append(self._end)

		data_out.extend(file_data)

		#total data length to be hidden + 6 bytes padding for channel encoding
		#don't use alpha so 3 bits per byte need to store 16 bits so 6 bytes 

		#pad data length so we have enough to fulfill the iterations for the
		#number of channels
		if self.encrypt_data:
			try:
				f = Fernet(self.key)
			except Exception as err:
				raise IOError("ERROR - key not in correct format, check format or leave blank to get new auto generated key")
			
			data_out = bytearray(f.encrypt(bytes(data_out)))
			#get the length of the encrypted data and XOR it, fixed to length of 12
			if self.verbose >= 1:
				print("::Encrypting Data")
			if self.verbose >=3:
				print ("  Encrypted Data Length:",len(data_out))
			edata_length = bytearray()
			edata_length_bin = bin(len(data_out))[2:].zfill(40)
			if self.verbose >=3:
				print ("  Encrypted Data Length BIN:", edata_length_bin)

			edata_length.append(int(edata_length_bin[0:8],2))
			edata_length.append(int(edata_length_bin[8:16],2))
			edata_length.append(int(edata_length_bin[16:24],2))
			edata_length.append(int(edata_length_bin[24:32],2))		
			edata_length.append(int(edata_length_bin[32:40],2))

			if self.verbose >=3:
				print ("  Encrypted Data Length INT:", len(edata_length))


			edata_length = self.xor(edata_length,self.key)

			#add the encrypted data length to the front of the data
			edata_length.extend(data_out)

			data_out = edata_length


			if self.verbose >=3:
				print ("  Encrypted Header and data")


		data_length = len(data_out)
		#add 6 min, add 10 to pad for rounding errors etc. if needed
		image_length_required = data_length + 100
		



		if self.verbose >= 2:
			print ("  Data file successfully loaded:", input_file)
			print ("  Data file length in bytes:", len(file_data))
			print ("  Total Data length including headers in bytes:", data_length)
			print ("  Min Image Length required:", image_length_required)

		if len(image_file) > 0:
			hide_in_image = True
		else:
			hide_in_image = False

		#if we have an image path try and open it
		if hide_in_image:
			try:
				im = Image.open(image_file)
			except IOError as err:
				raise IOError ("ERROR - Unable to open image file to hide data in, check file path and file type (supplied'{0}'), see below for full error details.\n{1}".format(image_file,err))


			if self.verbose >= 2:
				print ("  Original Image type:", im.mode)

			#does the image have an alpha channel
			#if it does and we are just writing RGB that's fine leave it alone so we don't screw the image up
			#but make a note as we will get 4 tuples back not 3, convert to RGBA just to be
			#on the safe side as well so we know what we are working with

			if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
				if im.mode != "RGBA":
					im = im.convert("RGBA")
				read_image_as = "RGBA"
			else:
				#it didn't have an alpha channel but we need one so
				#convert it to RGBA
				if self.output_image_type == "RGBA":
					im = im.convert("RGBA")
					read_image_as = "RGBA"

				#just in case er have L or CKMY or whatever, we know there is no transparency at this point
				elif self.output_image_type == "RGB" and im.mode != "RGB":
					im = im.convert("RGB")
					read_image_as = "RGB"
				#has to be RGB by now dont convert it just set image type
				else:
					read_image_as = "RGB"
				#now check what we want to output, we may


			#resize the image to it fits the data to allow even distribution of the data.
			#change length to data into bits (image_length*8)
			#divide image_length in bits by the number of bits we are going to store in each pix (self.number_of_bits)
			#this gives us the min number of pix required to store the data
			#best way to figure out new aspect ratio size


			if resize_image:
				#optimum_image_size = int(math.ceil(math.sqrt((image_length*8)/self.number_of_bits)))
				#get size of the image
				if self.verbose >= 1:
					print("::Resizing Image to fit to data")
				iw,ih = im.size
				image_number_of_px = iw*ih
				data_number_of_px = (image_length_required*8)/self.number_of_bits
				#calculate ratio factor
				i_f = math.sqrt((data_number_of_px/2)/(image_number_of_px/2))
				imw = int(math.ceil(iw * i_f))
				imh = int(math.ceil(ih * i_f))
				i_s = (imw,imh)
				im = im.resize(i_s,Image.LANCZOS)
			else:
				imw,imh = im.size
				iw, ih = imw, imh
				if math.ceil((image_length_required*8)/self.number_of_bits) > imw*imh:
					raise IOError ("ERROR - Image is not big enough to hide data in, select auto resize and the image will be adjusted")



			if self.verbose >= 2:
				print("  Loaded Image:", image_file)
				print("  Output Image type:", im.mode)
				print("  Read Image As:", read_image_as)
				print("  Original Image size: width {0}, height {1}".format(iw,ih))
				print("  New Size to accommodate data: width {0}, height {1}".format(imw,imh))

		#create a square blank image
		else:
			if self.verbose >= 1:
				print("::Creating Image to put data in")
			imw = imh = int(math.ceil(math.sqrt((image_length_required*8)/self.number_of_bits)))
			im = Image.new(self.output_image_type, (imw,imh))
			read_image_as = self.output_image_type
			if self.verbose >= 2:
				print("No Image supplied, created image to accommodate data: width {0}, height {1}".format(imw,imh))
				print("Set image type to '{0}' to accommodate channels".format(self.output_image_type))




		#16 bits needed for channel data
		lead_in = 0
		lead_in_string = ''

		#get lowest 4 bytes padded with leading 0 for 4 channels
		#never higher than 8
		for i in self.chan:
			lead_in_string += (bin(i)[2:].zfill(4))

		if self.verbose >= 3:
			print("  Channel Lead-in String:", lead_in_string)

		if self.encrypt_data:
			#use the key provided to do an additional xor encryption
			#on the two lead in bytes on how to read they data out of the image
			lead_in_string = self.enc_dec_header(lead_in_string)

			if self.verbose >= 3:
				print("  Encrypted Channel Lead-in String:", lead_in_string)

		#pad lead_in_string to 18 to make it divisible by 3 nicely
		lead_in_string += "00"


		#start of dat not taking into account the lead 16 bytes
		data_position = 0

		#create 0 padded byte strings from byte data
		str_working_bytes = ''

		red = 0
		green = 0
		blue = 0
		alpha = 0

		#end of data stream
		eod = 0
		#if we are not going to be able to complete the last run we don't have an exact bit mapping to bytes


		#####TO-DO write something clever with numpy this is a very slow way of doing it but it works for now#####
		if self.verbose >= 1:
			print("::Writing data to Image")
		for h in range(imh):
			for w in range(imw):
				if self.verbose >= 1:
					sys.stdout.write("\r::Progress: {0}%".format(math.ceil((h/imh)*100)))
					sys.stdout.flush()
				#if we are hiding in a picture
				#get current color for px
				if hide_in_image:
					if read_image_as == 'RGBA':
						rd, gr, bl, al = im.getpixel((w,h))
					else:
						rd, gr, bl = im.getpixel((w,h))

				#first set channel header always  going to be space for header so no eof checks needed
				if lead_in < 6:
					#store lead in in RGB regardless of rest of byte distribution
					#always one bit per channel
					if hide_in_image:
						rd = self.replacebits(rd, lead_in_string[0])
						gr = self.replacebits(gr, lead_in_string[1])
						bl = self.replacebits(bl, lead_in_string[2])
						#leave al as is and rewrite it if its there
					else:
						rd = int(lead_in_string[0])
						gr = int(lead_in_string[1])
						bl = int(lead_in_string[2])
						al = 255
					if self.verbose >=3:
						if read_image_as == 'RGBA':
							print("Lead In string rd,gr,bl,al,iteration,next string:",rd,gr,bl,al,lead_in,lead_in_string)
						else:
							print("Lead In string rd,gr,bl iteration,next string:",rd,gr,bl,lead_in,lead_in_string)
					lead_in += 1
					lead_in_string = lead_in_string[3:]
					#now we write the data
					if read_image_as == "RGBA":
						im.putpixel((w,h), (rd,gr,bl,al))
					#we know because of previous logic the only other option is now RGB, if it was some other format
					#like gray scale we converted it to RGB earlier, if the hide image was RGB and we wanted to use the alpha channel
					#then read image would have been set to RGBA earlier.
					else:
						im.putpixel((w,h), (rd,gr,bl))

				else:
					#if there is more data available or we still have data to process
					if not eod or len(str_working_bytes) > 0:
						#fill the working string until we have enough data to do one iteration
						#there may be some bits left over pad each byte string so its always represents 8 bits
						while len(str_working_bytes) <= self.number_of_bits and data_position < data_length:
							str_working_bytes += bin(data_out[data_position])[2:].zfill(8)
							data_position += 1
							#if we reach the end of the data exit while loop regardless of if the string is full or not
							#set flag for end of data reached
							if data_position >= data_length:
								#we have all the available bits end while set end of file
								eod = 1
								break
						#if we have reached the end but the string still has some data in it
						#make sure there is enough to complete a run
						if eod and len(str_working_bytes) < self.number_of_bits:
							#pad out string with 0's to bit length to it does not error
							str_working_bytes = str_working_bytes.ljust(self.number_of_bits,'0')

						#now set the bits we want to store for each channel
						#if its a channel we are not using set to empty string
						#which will just cause current byte to be used.
						if self.verbose >= 4:
							print("Working Bytes, position, data length",str_working_bytes,data_position,data_length)

						if self.chan[self._r] > 0:
							red = str_working_bytes[0:self.chan[self._r]]
							str_working_bytes = str_working_bytes[self.chan[self._r]:]
						else:
							red = ''
						if self.chan[self._g] >0:
							green = str_working_bytes[0:self.chan[self._g]]
							str_working_bytes = str_working_bytes[self.chan[self._g]:]
						else:
							green = ''
						if self.chan[self._b] > 0:
							blue = str_working_bytes[0:self.chan[self._b]]
							str_working_bytes = str_working_bytes[self.chan[self._b]:]
						else:
							blue = ''
						if self.chan[self._a] > 0:
							alpha = str_working_bytes[0:self.chan[self._a]]
							str_working_bytes = str_working_bytes[self.chan[self._a]:]
						else:
							alpha = ''
						#now set to the px we are at
						#does not matter if its hide in linage or not we will use the
						#same logic, just need to check if we are writing alpha or not

						#if we are reading an rbga image then write one back out with the alpha so it looks the same
						#regardless of if we are adding data in there.

						if read_image_as == "RGBA":
							rd = self.replacebits(rd,red)
							gr = self.replacebits(gr,green)
							bl = self.replacebits(bl,blue)
							al = self.replacebits(al,alpha)
							im.putpixel((w,h), (rd,gr,bl,al))

						#we know because of previous logic the only other option is now RGB, if it was some other format
						#like gray scale we converted it to RGB earlier, if the hide image was RGB and we wanted to use the alpha channel
						#then read image would have been set to RGBA earlier.
						else:
							rd = self.replacebits(rd,red)
							gr = self.replacebits(gr,green)
							bl = self.replacebits(bl,blue)
							im.putpixel((w,h), (rd,gr,bl))
					
					#spare bytes we don't need, just replace with same bytes if replace with image
					#pad with 0 etc. if just making a square image
					else:
						if read_image_as == "RGBA":
							if hide_in_image:
								im.putpixel((w,h), (rd,gr,bl,al))
							else:
								#pick random pix to pad so you can see where end of data is in image
								im.putpixel((w,h), im.getpixel((random.randint(0,w),random.randint(0,h))))
						else:
							if hide_in_image:
								im.putpixel((w,h), (rd,gr,bl))
							else:
								#pick random pix to pad so you can see where end of data is in image
								im.putpixel((w,h), im.getpixel((random.randint(0,w),random.randint(0,h))))
		if self.verbose >=1:
			sys.stdout.write("\r::Progress: 100%")
			sys.stdout.flush()
		try:
			im.save(self.output_file, optimize = True)
			if self.verbose >=1:
				print("")
				print("::Image '{0}'' created and saved".format(self.output_file))
			if self.magic_header != 'XYZZY':
				if self.verbose >=1:
					print("***YOU SELECTED A CUSTOM MAGIC HEADER KEEP IT SAFE YOU CAN'T DECODE WITHOUT IT***")
					print("::Magic Header:",self.magic_header)
			if self.encrypt_data:
				if self.verbose >=1:
					print("")
					print("***KEEP THIS KEY SAFE YOU CANT DECRYPT WITHOUT IT***")
					print("")
					print("***if your key starts with a - and you are using the example main class explicitly reference it in the command line with -k='-your key starting with a -'***")
					print("")
					print("::")
					print("::Decrypt Key:",self.key.decode('utf-8'))
					print("::")


		except IOError as err:
			raise IOError ("ERROR - Unable to save image file check file path / permissions (supplied'{0}'), see below for full error details.\n{1}".format(output_file,err))

	def decode(self,image_file,key='',output_file='',magic_header='XYZZY'):
		"""Store any file in any image as a png file.

		:param str image_file: the image file you want to try and decode, needs to be PNG, will error if it can't find any hidden data.
		:param str key: if the file was encrypted supply the key as a text string here
		:param str output_file: this is the output file path, by default the code will extract to the same path as it is run
			and won't warn if theres an overwrite, if you want to extract somewhere else put the path here.
		:param str magic_header: if the magic header had been changed you need to put it here, default will suffice in most cases.
		:raises IOError: if it can't read or write any of the files successfully.
		
		Example usage see :py:func:`~ManipulateImage.encode` for an example not using encryption::
			
			>>> pnc = pncase.ManipulateImage(verbose=1,encrypt_data=True)
			>>> pnc.encode(input_file='medium_test')
			::encode::
			::Reading Datafile: pillowncase/pillowncase/files/pg29809.txt
			::Encrypting Data
			::Resizing Image to fit to data
			::Writing data to Image
			::Progress: 100%
			::Image 'pNcase.png'' created and saved

			***KEEP THIS KEY SAFE YOU CANT DECRYPT WITHOUT IT***

			***if your key starts with a - and you are using the example main class explicitly
				reference it in the command line with -k='-your key starting with a -'***

			::
			::Decrypt Key: 89DWqGN5wX_5-g7QBO8egn2sBqd2Ii4DifHngnF43ZQ=
			::
			>>> pnc.decode(image_file='pNcase.png',key='89DWqGN5wX_5-g7QBO8egn2sBqd2Ii4DifHngnF43ZQ=')
			::Decode::
			::Opened Image-file: pNcase.png
			::Reading data from Image
			::Progress: 100%
			::Decrypting Data
			::Using Key: 89DWqGN5wX_5-g7QBO8egn2sBqd2Ii4DifHngnF43ZQ=
			::Found hidden file: pg29809.txt
			::Successfully read data
			::All done Data Written to file: pg29809.txt
		"""


		if self.verbose >=1:
			print("::Decode::")
		
		if magic_header != 'XYZZY':
			self.magic_header = magic_header
			if self.verbose >= 2:
				print("  Magic Header:", self.magic_header)

		if len(key) > 0:
			self.encrypt_data = True
			self.key = str.encode(key,'utf-8')
		
		try:
			im = Image.open(image_file)
		except IOError as err:
			raise IOError ("ERROR - Unable to open image file, check file path and file type (supplied'{0}'), see below for full error details.\n{1}".format(image_file,err))

		#get image size
		imw , imh = im.size
		read_image_as = im.mode
		#take of lead 6 bytes - remember -6 in case it catches me out later
		data_length = (imw*imh)

		if self.verbose >=1:
			print("::Opened Image-file: {0}".format(image_file))
		if self.verbose >=2:
			print ("  Image size w,h:",imw,imh)
			print("  Image Mode:",read_image_as)
			print("  Total Data Length:",data_length)
		
		if read_image_as != "RGBA" and read_image_as != "RGB":
			raise IOError("ERROR - Image must be RGBA or RGB, supplied {0}".format(read_image_as))
		#first read first 6 bits
		lead_in = 0
		lead_in_string = ''

		data_bytes = bytearray()
		file_name = bytearray()
		output_data_length = bytearray()
		output_file_name = ''
		data_length_offset = 0
		str_working_bytes = ''
		output_data = bytearray()
		
		#####TO-DO write something clever with numpy this is a very slow way of doing it but it works for now#####
		if self.verbose >=1:
			print("::Reading data from Image")
		for h in range(imh):
			if self.verbose >=1:
				sys.stdout.write("\r::Progress: {0}%".format(math.ceil((h/imh)*100)))
				sys.stdout.flush()
			for w in range(imw):
				if read_image_as == 'RGBA':
					rd, gr, bl, al = im.getpixel((w,h))
				else:
					rd, gr, bl = im.getpixel((w,h))
				
				if data_length < 6:
					raise IOError("ERROR - Image data length to small decode not possible {0}".format(data_length))
				#only ever going to be last bit in RGB so ignore alpha if there
				if lead_in < 6:
					lead_in_string += str(rd & 1)
					lead_in_string += str(gr & 1)
					lead_in_string += str(bl & 1)
					lead_in += 1
					if self.verbose >=2:
						print("Lead In string:", lead_in_string)					
						#if we have all lead in data set the channels
					if lead_in == 6:
						if self.encrypt_data:
							lead_in_string = self.enc_dec_header(lead_in_string)

							if self.verbose >=2:
								print("Decrypted Lead In string:", lead_in_string)	


						self.chan[self._r] = int(lead_in_string[0:4],2)
						self.chan[self._g] = int(lead_in_string[4:8],2)
						self.chan[self._b] = int(lead_in_string[8:12],2)
						self.chan[self._a] = int(lead_in_string[12:16],2)
						if self.verbose >=2:
							print("Channels set to (RGBA):",self.chan)
						for i in self.chan:
							if i > 8:
								raise IOError("ERROR - Either hidden data is encrypted and you have the wrong key or there is no data hidden in this image, channel value over 8")
						if self.chan[self._a] >0 and read_image_as == "RGB":
							raise IOError("ERROR - Either hidden data is encrypted and you have the wrong key or there is no data hidden in this image, alpha channel specified but image is RGB")
					


	
				#if not lead in read rest of the data using lead in data to change back to bytes
				else:		
					#process each pixel
					#if its a channel get the last number of bits specified and add to string
					if self.chan[self._r] >0:
						str_working_bytes += bin(rd)[2:].zfill(8)[-self.chan[self._r]:]
					if self.chan[self._g] >0:
						str_working_bytes += bin(gr)[2:].zfill(8)[-self.chan[self._g]:]
					if self.chan[self._b] >0:
						str_working_bytes += bin(bl)[2:].zfill(8)[-self.chan[self._b]:]
					if self.chan[self._a] >0:
						str_working_bytes += bin(al)[2:].zfill(8)[-self.chan[self._a]:]
					#once we have more than 8 bits convert to bytes and 
					#add to byte array
					while len(str_working_bytes) >= 8:
						data_bytes.append(int(str_working_bytes[0:8],2))
						str_working_bytes = str_working_bytes[8:]
		if self.verbose >=1:
			sys.stdout.write("\r::Progress: 100%")
			sys.stdout.flush()

		#if we are going to try and decrypt
		if self.verbose >=3:
			print("")
			print ("Data length before Decryption:", len(data_bytes))
			print ("working bytes",str_working_bytes)

		if self.encrypt_data:
			if self.verbose >=1:
				print("")
				print("::Decrypting Data")
				print("::Using Key:",self.key.decode('utf-8'))
			try:
				f = Fernet(self.key)
			except Exception as err:
				raise IOError("ERROR - key not in correct format, check format and try again")
			
			try:
				edata_length = self.xor(data_bytes[0:5],self.key)
				edata_length_bin = ""

				for i in edata_length:
					edata_length_bin += bin(i)[2:].zfill(8)

				if self.verbose >=3:
					print ("Recovered data length value:",int(edata_length_bin,2))				
					print ("Data length retrieved BIN:", edata_length_bin)


			except Exception as err:
				raise IOError("ERROR - unable to extract data length from encrypted stream")
			#print(data_bytes[5:int(edata_length_bin,2)+5])
			try:
				#decrypt the rest
				#edata_length_bin is the length stored from the encrypt
				data_bytes = bytearray(f.decrypt(bytes(data_bytes[5:int(edata_length_bin,2)+5])))

			except Exception as err:
				raise IOError("ERROR - key is correct format but does not match digest, either not an encrypted image or you have the wrong key or data length {0}",int(edata_length_bin,2)+5,err)

			if self.verbose >=2:
				print("  Decrypted Header and Data:")


		#now we have all the data can we read it
		data_length = len(data_bytes)
		
		if self.verbose >=3:
			print ("Data length after Decryption:", len(data_bytes))
		#check the header matches
		
		header_length = len(self.magic_header.encode('utf-8'))
		data_position = 0

		try:
			if data_bytes[0:header_length].decode('utf-8') != self.magic_header:
				raise IOError("ERROR - Could not match magic header, found {0}, expected {1}".format(data_bytes[0:header_length].decode('utf-8'),self.magic_header))
		except Exception as err:
			raise IOError("ERROR - Unable to decode magic header, hidden data is either encrypted or there is none")
		data_position = header_length
		if self.verbose >=2:
			print("  Found Magic Header:", self.magic_header)
		#next we should see the file name can be any length
		if data_bytes[data_position] != self._start:
			raise IOError("ERROR - Could not find filename start flag")
		#ok we have found the start
		data_position += 1
		while data_bytes[data_position] != self._end:
			file_name.append(data_bytes[data_position])
			data_position += 1
			if data_position == data_length:
				#bail EOF and no close out for file name
				raise IOError("ERROR - Could not find filename end flag")
		output_file_name = file_name.decode('utf-8')
		if self.verbose >=2:
			print("  Found File Name:", output_file_name)
		#ok we have the file name
		#next we should see the data length value
		data_position += 1
		if data_bytes[data_position] != self._start:
			raise IOError("ERROR - Could not find file length start flag")
		#ok we have found the start
		data_position += 1
		
		while data_bytes[data_position] != self._end:
			output_data_length.append(data_bytes[data_position])
			data_position += 1
			if data_position == data_length:
			#bail EOF and no close out for data length
				raise IOError("ERROR - Could not find file length end flag")

		#have the datapackage length
		data_position += 1
		data_length_offset = int(output_data_length.decode('utf-8')) + data_position
		if self.verbose >=2:
			print("  Expected Data Length:", int(output_data_length.decode('utf-8')))		
		#read data
		if data_length_offset > data_length:
			raise IOError("ERROR - Expected data length would exceed file size",data_length_offset,data_length)
		if self.verbose >=1:
			print("::Found hidden file:",output_file_name)
		#write core data
		output_data.extend(data_bytes[data_position:data_length_offset])
		if self.verbose >=1:
			print ("::Successfully read data")
		if output_file != '':
			output_file_name = os.path.join(output_file,output_file_name)

		try:
			open(output_file_name, 'wb').write(output_data)
		except Exception as err:
			raise IOError("ERROR - Unable to save data file",err)

		self.data_output_file = output_file_name
		if self.verbose >=1:
			print("::All done Data Written to file:",output_file_name)

