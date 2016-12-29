import random
import sys
import os


class RandomUTF_8String:

	def __init__(self):
		input_file = os.path.join(os.path.dirname(__file__), "utf8_sequence_0-0x10ffff_assigned_printable_unseparated.txt")
		with open(input_file, "rb") as binary_file:
			file_data = binary_file.read()
			self.utf_8_data = file_data.decode('utf-8')
			self.utf_8_data_random_range = len(self.utf_8_data)-1

	def getStringRandomLength(self,length=20):
		l = random.randint(2,length)
		s=''

		for i in range(1,l):
			s+= self.utf_8_data[random.randint(0,self.utf_8_data_random_range )]
		return s

	def getStringFixedLength(self,length=20):
		l = length
		s=''

		for i in range(1,l):
			s+= self.utf_8_data[random.randint(0,self.utf_8_data_random_range )]
		return s

