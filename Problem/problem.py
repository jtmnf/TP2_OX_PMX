import os.path as op

import numpy as np


class ProblemRepresentation(object):
	def __init__(self, nCities=10, nItems=3, instance=1, tight=25, path='\\DataSet\\'):
		self.numCities = nCities
		self.numItems = nItems
		self.instance = instance
		self.tight = tight
		self.knapsackWeight = None
		self.vmax = None
		self.vmin = None
		self.knapsackRent = None
		self.dists = list()
		self.items = list()
		self.available = list()  # self.available[city][item]  -- isto esta errado (?) , sera self.available[item][city]

		self.readInput(
			path + str(self.numCities) + "\\" + str(nCities) + "_" + str(nItems) + "_" + str(instance) + "_" + str(
				tight))

	def _optimizeTypes(self):
		self.dists = np.array(self.dists)
		self.items = np.array(self.items)
		self.available = np.array(self.available)

	def readInput(self, fname):
		"""
		Credits to J.F.Sebastian from StackOverflow
		http://stackoverflow.com/questions/3277503/python-read-file-line-by-line-into-array
		:param fname: File path and name
		:return:
		"""
		with open(op.dirname(op.dirname(__file__)) + fname + ".txt") as f:
			content = [line.rstrip('\n') for line in f.readlines()]
		self.knapsackWeight = float(content[2])
		self.vmax = float(content[3])
		self.vmin = float(content[4])
		self.knapsackRent = float(content[5])

		# Read cities distances
		usefulContent = content[6:]
		for i in range(self.numCities):
			distanciesStr = usefulContent[i].split()
			self.dists.append([float(x) for x in distanciesStr])

		# Remove non useful information
		usefulContent = usefulContent[self.numCities:]
		# Read items weight and value
		weight = [float(x) for x in usefulContent[0].split()]
		value = [float(x) for x in usefulContent[1].split()]

		for i in range(self.numItems):
			self.items.append(Item(weight[i], value[i]))

		# Remove non useful information
		usefulContent = usefulContent[2:]
		# Read availability
		for i in range(self.numItems):
			self.available.append([bool(int(x)) for x in usefulContent[i].split()])

		self._optimizeTypes()


class Item(object):
	def __init__(self, weight, value):
		self.weight = weight
		self.value = value

	def __cmp__(self, other):
		if self.weight == other.weight and self.value == other.value:
			return True
		return False
