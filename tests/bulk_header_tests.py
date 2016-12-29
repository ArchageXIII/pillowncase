from nose.tools import *
from pillowncase import pncase
import os
import shutil
from datetime import datetime
import random
import hashlib
from tests import helper
from tests import header_tests
import sys




def setup():
    print ("SETUP!")
    helper.setup_environment()


def teardown():
    print ("TEAR DOWN!")


def test_Header_CC_bulk():

	i=0
	while i < 10:
		header_tests.test_Header_CC_hide_random_data_create_image()
		header_tests.test_Header_CC_e_hide_random_data_create_image()
		header_tests.test_Header_CC_hide_random_data_use_image()
		header_tests.test_Header_CC_e_hide_random_data_use_image()
		i += 1
