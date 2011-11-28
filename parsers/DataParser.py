# coding: utf-8

__author__ = "Alexander Soulimov (alexander.soulimov@gmail.com)"
__copyright__ = "Copyright (c) 2011 A.Soulimov"
__license__ = "Python"


def get_objects(file_lines):
	"""
	First line - attribute names
	Other lines - objects
	"""

	attr_names = file_lines[0].split(",")

	objects = list()

	for line in file_lines[1:]:
		obj = dict()
		attr_values = line.split(",")
		for i in range(0, len(attr_values)):
			key = attr_names[i].replace('\n', '')
			value = attr_values[i].replace('\n', '')
			obj[key.strip()] = value.strip()
		objects.append(obj)
	return objects


if __name__ == "__main__":
	print get_objects(["attr1, attr2, attr3, attr4?\n", "val11, val12, val13, val14\n", "val21,val22,val23,val4"])



