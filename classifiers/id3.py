# coding: utf-8
import math

__author__ = "Alexander Soulimov (alexander.soulimov@gmail.com)"
__copyright__ = "Copyright (c) 2011 A.Soulimov"
__license__ = "Python"

def entropy(data, target_attr):
	"""
	Вычисляем энтропию набора объектов для заданного атрибута
	"""
	val_freq = {}
	data_entropy = 0.0

	# Вычисляем частоту встречаемости каждого значения атрибута в наборе данных
	for record in data:
		key = record[target_attr]
		if val_freq.has_key(key):
			val_freq[key] += 1.0
		else:
			val_freq[key] = 1.0

	# Вычисляем само значение энропии
	for freq in val_freq.values():
		data_entropy += (-freq / len(data)) * math.log(freq / len(data), 2)

	return data_entropy


def gain(data, attr, target_attr):
	"""
	Вычисляем уменьшение энтропии
	"""
	val_freq = {}
	subset_entropy = 0.0

	# Вычисляем частоту встречаемости каждого значения атрибута в наборе данных
	for record in data:
		key = record[target_attr]
		if val_freq.has_key(key):
			val_freq[key] += 1.0
		else:
			val_freq[key] = 1.0

	# Calculate the sum of the entropy for each subset of records weighted
	# by their probability of occuring in the training set.
	for val in val_freq.keys():
		val_prob = val_freq[val] / sum(val_freq.values())
		data_subset = [record for record in data if record[attr] == val]
		subset_entropy += val_prob * entropy(data_subset, target_attr)

	# Subtract the entropy of the chosen attribute from the entropy of the
	# whole data set with respect to the target attribute (and return it)
	return entropy(data, target_attr) - subset_entropy

