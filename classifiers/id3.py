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


def get_most_popular(data, attr):
	"""
	Поиск самого часто употребимого значения атрибута attr
	"""
	temp_attr = list()
	for d in data:
		temp_attr.append(d[attr])

	temp_unique = set(temp_attr)

	max_freq = 0
	result = None

	for t in temp_unique:
		if temp_attr.count(t) > max_freq:
			result = t
			max_freq = temp_attr.count(t)
	return result

def get_values(data, attr):
	"""
	Creates a list of values in the chosen attribut for each record in data,
	prunes out all of the redundant values, and return the list.
	"""
	data = data[:]
	return list(set([record[attr] for record in data]))

def choose_attribute(data, attributes, target_attr, fitness):
	"""
	Cycles through all the attributes and returns the attribute with the
	highest information gain (or lowest entropy).
	"""
	data = data[:]
	best_gain = 0.0
	best_attr = None

	for attr in attributes:
		gain = fitness(data, attr, target_attr)
		if gain >= best_gain and attr != target_attr:
			best_gain = gain
			best_attr = attr

	return best_attr

def get_examples(data, attr, value):
	"""
	Returns a list of all the records in <data> with the value of <attr>
	matching the given value.
	"""
	data = data[:]
	rtn_lst = []

	if not data:
		return rtn_lst
	else:
		record = data.pop()
		if record[attr] == value:
			rtn_lst.append(record)
			rtn_lst.extend(get_examples(data, attr, value))
			return rtn_lst
		else:
			rtn_lst.extend(get_examples(data, attr, value))
			return rtn_lst


def create_decision_tree(data, fitness_func=gain):
	"""
	Создание дерева принятия решения
	"""
	data = data[:]
	target_attr = None
	attributes = list()
	for key in data[0].keys():
		if '?' in key:
			target_attr = key
		attributes.append(key)
	vals = [record[target_attr] for record in data]
	default = get_most_popular(data, target_attr)
	
	# If the dataset is empty or the attributes list is empty, return the
	# default value. When checking the attributes list for emptiness, we
	# need to subtract 1 to account for the target attribute.
	if not data or (len(attributes) - 1) <= 0:
		return default
	# If all the records in the dataset have the same classification,
	# return that classification.
	elif vals.count(vals[0]) == len(vals):
		return vals[0]
	else:
		# Choose the next best attribute to best classify our data
		best = choose_attribute(data, attributes, target_attr, fitness_func)

		# Create a new decision tree/node with the best attribute and an empty
		# dictionary object--we'll fill that up next.
		tree = {best:{}}

		# Create a new decision tree/sub-node for each of the values in the
		# best attribute field
		for val in get_values(data, best):
			# Create a subtree for the current value under the "best" field
			subtree = create_decision_tree(
				get_examples(data, best, val),
				[attr for attr in attributes if attr != best],
				target_attr,
				fitness_func)

			# Add the new subtree to the empty dictionary object in our new
			# tree/node we just created.
			tree[best][val] = subtree

	return tree