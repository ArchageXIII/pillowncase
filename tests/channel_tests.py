from nose.tools import *
from pillowncase import pncase
import os
import shutil
from datetime import datetime
import random
import hashlib
from tests import helper
import sys



verbose = 2

def setup():
    print ("SETUP!")
    helper.setup_environment()


def teardown():
    print ("TEAR DOWN!")

def test_CC_hide_random_data_create_image():

	try:
		input_file,input_file_name,input_file_hash = helper.create_data("hide_random_data_create_image")
		pnc = pncase.ManipulateImage(verbose=verbose,custom_channels=helper.get_random_channel_string())
		pnc.encode(input_file=input_file,output_file=input_file)
		output_file_path = os.path.join("tmp_tests","output_test_data")
		pnc.decode(image_file=pnc.get_output_file(),output_file=output_file_path)
		output_file_hash = helper.get_file_hash(os.path.join(output_file_path, input_file_name))
		assert input_file_hash == output_file_hash
		#test ran fine delete the test files
		helper.clean_test_files(pnc)
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise

def test_CC_e_hide_random_data_create_image():


	try:
		input_file,input_file_name,input_file_hash = helper.create_data("e_hide_random_data_create_image")
		pnc = pncase.ManipulateImage(encrypt_data=True,verbose=verbose,custom_channels=helper.get_random_channel_string())
		pnc.encode(input_file=input_file,output_file=input_file)
		output_file_path = os.path.join("tmp_tests","output_test_data")
		pnc.decode(image_file=pnc.get_output_file(),output_file=output_file_path,key=pnc.get_key())
		output_file_hash = helper.get_file_hash(os.path.join(output_file_path, input_file_name))
		assert input_file_hash == output_file_hash
		helper.clean_test_files(pnc)
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
def test_CC_hide_random_data_use_image():
	try:
		input_file,input_file_name,input_file_hash = helper.create_data("hide_random_data_use_image")
		pnc = pncase.ManipulateImage(verbose=verbose,custom_channels=helper.get_random_channel_string())
		pnc.encode(input_file=input_file,output_file=input_file,image_file=os.path.join("pillowncase","files","pNcase.png"))
		output_file_path = os.path.join("tmp_tests","output_test_data")
		pnc.decode(image_file=pnc.get_output_file(),output_file=output_file_path)
		output_file_hash = helper.get_file_hash(os.path.join(output_file_path, input_file_name))
		assert input_file_hash == output_file_hash
		helper.clean_test_files(pnc)
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
def test_CC_e_hide_random_data_use_image():

	try:
		input_file,input_file_name,input_file_hash = helper.create_data("e_hide_random_data_use_image")
		pnc = pncase.ManipulateImage(encrypt_data=True,verbose=verbose,custom_channels=helper.get_random_channel_string())
		pnc.encode(input_file=input_file,output_file=input_file,image_file=os.path.join("pillowncase","files","pNcase.png"))
		output_file_path = os.path.join("tmp_tests","output_test_data")
		pnc.decode(image_file=pnc.get_output_file(),output_file=output_file_path,key=pnc.get_key())
		output_file_hash = helper.get_file_hash(os.path.join(output_file_path, input_file_name))
		assert input_file_hash == output_file_hash
		helper.clean_test_files(pnc)
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise