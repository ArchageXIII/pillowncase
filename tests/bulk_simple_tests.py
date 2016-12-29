from nose.tools import *
from pillowncase import pncase
import os
import shutil
from datetime import datetime
import random
import hashlib
from tests import helper
from tests import simple_tests
import sys



def setup():
    print ("SETUP!")
    helper.setup_environment()


def teardown():
    print ("TEAR DOWN!")

def test_bulk():

	i=0
	while i < 10:
		simple_tests.test_hide_random_data_create_image()
		simple_tests.test_e_hide_random_data_create_image()
		simple_tests.test_hide_random_data_use_image()
		simple_tests.test_e_hide_random_data_use_image()
		i += 1
