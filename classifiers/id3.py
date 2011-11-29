# coding: utf-8
import math

__author__ = "Alexander Soulimov (alexander.soulimov@gmail.com)"
__copyright__ = "Copyright (c) 2011 A.Soulimov"
__license__ = "Python"

def entropy(data, target_attr):
	"""
	Вычисляем энтропию набора объектов для заданного атрибута
	ЧЕМ МЕНЬШЕ ТЕМ ЛУЧШЕ
	@param data: тестовый набор данных
	@param target_attr: классифицируемый атрибут
	@return: значение энтропии для заданного атрибута
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
	Вычисляем разность энропий
	ЧЕМ БОЛЬШЕ ТЕМ ЛУЧШЕ

	@param data: тестовый набор данных
	@param attr: анализируемый атрибут
	@param target_attr: классифицируемый атрибут
	@return: значение энтропии для заданного атрибута
	"""
	val_freq = {}
	subset_entropy = 0.0

	# Вычисляем частоту появления каждого значения атрибута
	for record in data:
		if val_freq.has_key(record[attr]):
			val_freq[record[attr]] += 1.0
		else:
			val_freq[record[attr]] = 1.0

	# Вычисляем энропию для подмножества объектов
	# имеющих соответсвующее значение атрибута
	for val in val_freq.keys():
		val_prob = val_freq[val] / sum(val_freq.values())
		data_subset = [record for record in data if record[attr] == val]
		subset_entropy += val_prob * entropy(data_subset, target_attr)

	# Получаем разность энтропии анализируемого атрибута и вычисленного значения
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

def get_attr_values(data, attr):
	"""
	Получаем все значения атрибута
	"""
	return list(set([record[attr] for record in data]))

def choose_attribute(data, attributes, target_attr, fitness):
	"""
	Получаем самый подходящий атрибут для дальнейшей классификации
	ЧЕМ БОЛЬШЕ ТЕМ ЛУЧШЕ
	"""
	best_gain = 0.0
	best_attr = None

	for attr in attributes:
		gain = fitness(data, attr, target_attr)
		if gain >= best_gain and attr != target_attr:
			best_gain = gain
			best_attr = attr

	return best_attr

def get_objs_by_attr(data, attr, value):
	"""
	Получаем список объектов из тестового набора со значением атрибута attr равным value
	"""
	result = list()
	for obj in data:
		if obj[attr] == value:
			result.append(obj)
	return result

def create_decision_tree(data, attributes, target_attr, fitness_func=gain):
	"""
	Рекурсивная процедура создания дерева принятия решения
	"""
	vals = [record[target_attr] for record in data]
	default = get_most_popular(data, target_attr)
	
	if not data or (len(attributes) - 1) <= 0:
		return default
	# если все значения для данной ветки одинаковы (членить не надо)
	elif vals.count(vals[0]) == len(vals):
		return vals[0]
	else:
		# Получаем наиболее подходящий атрибут
		best = choose_attribute(data, attributes, target_attr, fitness_func)

		# создаем узел дерева
		tree = {best:{}}

		# Для каждого значения атрибута best
		# создать поддрево
		for val in get_attr_values(data, best):
			subtree = create_decision_tree(
							get_objs_by_attr(data, best, val),
							[attr for attr in attributes if attr != best],
							target_attr,
							fitness_func)
			tree[best][val] = subtree
	return tree


def start_creating_tree(data, fitness_func=gain):
	data = data[:]
	target_attr = None
	attributes = list()
	for key in data[0].keys():
		if '?' in key:
			target_attr = key
		attributes.append(key)
	return create_decision_tree(data, attributes, target_attr, fitness_func)