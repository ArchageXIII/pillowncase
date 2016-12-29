from nose.tools import *
from pillowncase import pncase
import os
import shutil
from datetime import datetime
import random
import hashlib



###helper clases

def get_time():

	return "-"+datetime.now().strftime("%Y%m%d-%H%M%S")+"-"

def create_data(test_name):
	file_name = test_name + get_time() + ".dat"
	file = os.path.join("tmp_tests","input_test_data",file_name)

	data = bytearray(os.urandom(random.randint(1,60000)))

	m = hashlib.md5()

	m.update(data)

	open(file, 'wb').write(data)

	return file,file_name,m.digest()


def get_file_hash(file_name):
	with open(file_name, "rb") as binary_file:
		file_data = binary_file.read()
	m = hashlib.md5()
	m.update(file_data)
	return m.digest()


def setup_environment():
	if not os.path.isdir("tmp_tests"):
		os.makedirs("tmp_tests")
		os.makedirs(os.path.join("tmp_tests","input_test_data"))
		os.makedirs(os.path.join("tmp_tests","output_test_data"))
		os.makedirs(os.path.join("tmp_tests","saved_test_data"))

def cleanup(test_script):
	if test_script == "simple_tests":
		pass
		# shutil.move("pNcase.png",os.path.join("tmp_tests","output_test_data",get_time()+"pNcase.png"))
		# shutil.move("pNcase_test.txt",os.path.join("tmp_tests","output_test_data",get_time()+"pNcase_test.txt"))

def get_random_channel_string():
	c = '0000'
	while c == '0000':
		c = str(random.randint(0,8))+str(random.randint(0,8))+str(random.randint(0,8))+str(random.randint(0,8))
	return c





def clean_test_files(pnc):
	output_file = ''
	input_file = ''
	data_output_file = ''

	try:
		output_file = pnc.get_output_file()
		os.remove(output_file)
	except:
		pass
	
	try:
		input_file = pnc.get_input_file()
		os.remove(input_file)
	except:
		pass
	
	try:
		data_output_file = pnc.get_data_output_file()
		os.remove(data_output_file)
	except:
		pass


def clean_default_test_files(pnc):
	output_file = ''
	# input_file = ''
	data_output_file = ''

	try:
		output_file = pnc.get_output_file()
		os.remove(output_file)
	except:
		pass
	
	# try:
	# 	input_file = pnc.get_input_file()
	# 	os.remove(input_file)
	# except:
	# 	pass
	
	try:
		data_output_file = pnc.get_data_output_file()
		os.remove(data_output_file)
	except:
		pass
