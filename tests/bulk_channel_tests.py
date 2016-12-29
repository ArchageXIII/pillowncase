from nose.tools import *
from pillowncase import pncase
import os
import shutil
from datetime import datetime
import random
import hashlib
from tests import helper
from tests import channel_tests
import sys




def setup():
    print ("SETUP!")
    helper.setup_environment()


def teardown():
    print ("TEAR DOWN!")


def test_CC_bulk():

	i=0
	while i < 10:
		channel_tests.test_CC_hide_random_data_create_image()
		channel_tests.test_CC_e_hide_random_data_create_image()
		channel_tests.test_CC_hide_random_data_use_image()
		channel_tests.test_CC_e_hide_random_data_use_image()
		i += 1
