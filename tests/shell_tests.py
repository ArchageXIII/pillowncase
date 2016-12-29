import os


def test_main_kitten():
	os.system("python pillowncase -f pillowncase/files/pNcase_test.txt -i kitten -o kitten_test.png -c RGBA -gg")
	os.system("python pillowncase -a decode -i kitten_test.png")
	#cleanup, leave to error as should be there if os call before worked
	os.remove("kitten_test.png")
	os.remove("pNcase_test.txt")

def test_main_katie():
	os.system("python pillowncase -f pillowncase/files/pNcase_test.txt -i katie -o katie_test.png -j 1230")
	os.system("python pillowncase -a decode -i katie_test.png")
	#cleanup, leave to error as should be there if os call before worked
	os.remove("katie_test.png")
	os.remove("pNcase_test.txt")

def test_default_main():
	os.system("python pillowncase")
	os.system("python pillowncase -a decode -i pNcase_small_test.png")
	#cleanup, leave to error as should be there if os call before worked
	os.remove("pNcase_small_test.png")
	os.remove("pNcase_test.txt")

def test_default_main_encrypt():
	os.system("python pillowncase -k f-V9So3g3PCAlKuKr8CQvAV7gjsEbUgy5p7Ra3brZpc=")
	os.system("python pillowncase -a decode -i pNcase_small_test.png -k f-V9So3g3PCAlKuKr8CQvAV7gjsEbUgy5p7Ra3brZpc=")
	#cleanup, leave to error as should be there if os call before worked
	os.remove("pNcase_small_test.png")
	os.remove("pNcase_test.txt")

def test_medium_main():
	os.system("python pillowncase -f medium_test")
	os.system("python pillowncase -a decode -i pNcase_medium_test.png")
	#cleanup, leave to error as should be there if os call before worked
	os.remove("pNcase_medium_test.png")
	os.remove("pg29809.txt")

def test_medium_main_encrypt():
	os.system("python pillowncase -f medium_test -k f-V9So3g3PCAlKuKr8CQvAV7gjsEbUgy5p7Ra3brZpc=")
	os.system("python pillowncase -a decode -i pNcase_medium_test.png -k f-V9So3g3PCAlKuKr8CQvAV7gjsEbUgy5p7Ra3brZpc=")
	#cleanup, leave to error as should be there if os call before worked
	os.remove("pNcase_medium_test.png")
	os.remove("pg29809.txt")

def test_large_main():
	os.system("python pillowncase -f large_test")
	os.system("python pillowncase -a decode -i pNcase_large_test.png")
	#cleanup, leave to error as should be there if os call before worked
	os.remove("pNcase_large_test.png")
	os.remove("bitshift.zip")

def test_large_main_encrypt():
	os.system("python pillowncase -f large_test -k f-V9So3g3PCAlKuKr8CQvAV7gjsEbUgy5p7Ra3brZpc=")
	os.system("python pillowncase -a decode -i pNcase_large_test.png -k f-V9So3g3PCAlKuKr8CQvAV7gjsEbUgy5p7Ra3brZpc=")
	#cleanup, leave to error as should be there if os call before worked
	os.remove("pNcase_large_test.png")
	os.remove("bitshift.zip")