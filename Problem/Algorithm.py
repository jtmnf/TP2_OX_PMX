import json
import pickle
import threading
import time
from operator import *
from random import *

import matplotlib

from Individual.population import *

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('ggplot')


class Algorithm:
	Maximization = 'maximize'
	Minimization = 'minimize'

	def __init__(self, oProblem, runs, numb_generations, tournament_size, sel_parents, sel_survivors,
	             elite_percent, fitness_func, TSPConfig, KPConfig, Hypermutation, plots, sizePop, emigrants,
	             optimization=Maximization):
		self.oProblem = oProblem
		self.runs = runs
		self.numb_generations = numb_generations
		self.tournament_size = tournament_size

		self.sel_parents = sel_parents
		self.sel_survivors = sel_survivors
		self.elite_percent = elite_percent
		self.fitness_func = fitness_func

		self.optimization = optimization

		self.TSPConfig = TSPConfig
		self.KPConfig = KPConfig

		self.StatBest = []
		self.StatAvg = []

		self.Hypermutation = Hypermutation

		self.plots = plots
		self.sizePop = sizePop
		self.emigrants = emigrants

	def _initializePop(self):
		self.oPopulation = Population(self.oProblem, self.sizePop)
		self.Population = [[[Indiv.cities, Indiv.items], 0] for Indiv in self.oPopulation.pop]

	def _initializePopReturn(self, sizePop):
		pop = Population(self.oProblem, sizePop, False)
		return [[[Indiv.cities, Indiv.items], 0] for Indiv in pop.pop]

	def _reverseOrder(self):
		return True if self.optimization == Algorithm.Maximization else False

	def _evalPopulation(self):
		self.Population = [[Indiv[0], self.fitness_func(Indiv[0])] for Indiv in self.Population]

	def _getPopulationAverage(self):
		return sum([fit for cromo, fit in self.Population]) / len(self.Population)

	def _getPopulationBest(self):
		_Population = self.Population
		_Population.sort(key=itemgetter(1), reverse=self._reverseOrder())
		return _Population[0]

	def tournament(self):
		size_pop = len(self.Population)
		MatePool = []
		_reverse = self._reverseOrder()
		for i in range(size_pop):
			Pool = sample(self.Population, self.tournament_size)
			Pool.sort(key=itemgetter(1), reverse=_reverse)
			MatePool.append(Pool[0])
		return MatePool

	def elitism(self, Offspring):
		_reverse = self._reverseOrder()
		size = len(self.Population)
		comp_elite = int(size * self.elite_percent)
		Offspring.sort(key=itemgetter(1), reverse=_reverse)
		self.Population.sort(key=itemgetter(1), reverse=_reverse)
		return self.Population[:comp_elite] + Offspring[:size - comp_elite]

	def immigration(self, sizePerctEmigrants):
		_reverse = self._reverseOrder()
		size = len(self.Population)
		comp_Pop = int(size * (1 - sizePerctEmigrants))
		self.Population.sort(key=itemgetter(1), reverse=_reverse)
		tmpPop = self._initializePopReturn(size - comp_Pop)
		return self.Population[:comp_Pop] + tmpPop

	def delayPacking(self, Indiv):
		_Indiv = Indiv[:]
		Cities = _Indiv[0][0]
		Items = _Indiv[0][1]
		_Items = Items[:]
		modified = False
		for item in Items:
			_item = item % self.oProblem.numItems
			for city in reversed(Cities):
				_city_item = self.oProblem.numItems * city + _item
				if _city_item == item:
					break

				if self.oProblem.available[_item][city] == True and _city_item not in _Items:
					del _Items[_Items.index(item)]
					_Items.append(_city_item)
					modified = True
					break

		_Items.sort()
		_Indiv[0][1] = _Items
		if modified == True:
			_Indiv[1] = self.fitness_func(_Indiv[0])
		return _Indiv

	def printTime(self):
		print()
		print(time.strftime("** TIME: %Y-%m-%d %H:%M:%S", time.gmtime()))
		print()

	def run(self):
		self.printTime()

		t = threading.Timer(360.0, self.printTime)
		t.start()

		self.StatBest = [None] * self.runs
		self.StatAvg = [None] * self.runs

		hypermutation_gen = self.Hypermutation['max_generations']

		for _run in range(self.runs):
			self._initializePop()
			size_pop = len(self.Population)
			print('Starting Run: ' + str(_run + 1))

			self._evalPopulation()

			self.StatBest[_run] = [self._getPopulationBest()[1]]
			self.StatAvg[_run] = [self._getPopulationAverage()]

			hypermutation_tail = 0
			diver = []
			maxDiver = []
			for i in range(self.numb_generations):
				if (i + 1) % 20 == 0:
					print('--Generation ' + str(i + 1))
				# print(str(i) + ' ' + str(self.StatBest[_run][-1]))

				hypermutation_tail += 1
				tsp_prob_cross = self.TSPConfig['prob_cross'][0]
				tsp_prob_mut = self.TSPConfig['prob_mut'][0]
				tsp_prob_variation_cross = self.TSPConfig['prob_variation_cross']
				tsp_prob_variation_mut = self.TSPConfig['prob_variation_mut']

				kp_prob_cross = self.KPConfig['prob_cross'][0]
				kp_prob_mut = self.KPConfig['prob_mut'][0]
				kp_prob_variation_cross = self.KPConfig['prob_variation_cross']
				kp_prob_variation_mut = self.KPConfig['prob_variation_mut']

				if self.Hypermutation['activate']:
					if hypermutation_tail > self.Hypermutation['generations']:

						count = 0
						for j in range(self.Hypermutation['generations']):
							if self.StatBest[_run][i - j] == self.StatBest[_run][-1]:
								count += 1

						if count == self.Hypermutation['generations'] or hypermutation_gen != self.Hypermutation[
							'max_generations']:
							hypermutation_gen -= 1
							if hypermutation_gen == 0:
								hypermutation_tail = 0
								hypermutation_gen = self.Hypermutation['max_generations']

							# print('*** Requrired hypermutation ' + str(i) + ' - ' + str(count))
							tsp_prob_mut = self.TSPConfig['prob_hmut']
							tsp_prob_variation_mut = False

							kp_prob_mut = self.KPConfig['prob_hmut']
							kp_prob_variation_mut = False
						else:
							tsp_prob_variation_mut = self.TSPConfig['prob_variation_mut']
							kp_prob_variation_mut = self.KPConfig['prob_variation_mut']

				# TODO: Para uma variaçao maior no final da geracao usar
				# TODO: Exemplo: tsp_prob_cross = self.TSPConfig['prob_cross'][0] - ((self.TSPConfig['prob_cross'][0] - self.TSPConfig['prob_cross'][1]) + (self.numb_generations - i))

				if tsp_prob_variation_cross:
					tsp_prob_cross = self.TSPConfig['prob_cross'][0] - (
						(self.TSPConfig['prob_cross'][0] - self.TSPConfig['prob_cross'][1]) * (
							i / self.numb_generations))

				if tsp_prob_variation_mut:
					tsp_prob_mut = self.TSPConfig['prob_mut'][0] + (
						(self.TSPConfig['prob_mut'][1] - self.TSPConfig['prob_mut'][0]) * (i / self.numb_generations))

				if kp_prob_variation_cross:
					kp_prob_cross = self.KPConfig['prob_cross'][0] - (
						(self.KPConfig['prob_cross'][0] - self.KPConfig['prob_cross'][1]) * (i / self.numb_generations))
				if kp_prob_variation_mut:
					kp_prob_mut = self.KPConfig['prob_mut'][0] + (
						(self.KPConfig['prob_mut'][1] - self.KPConfig['prob_mut'][0]) * (i / self.numb_generations))

				MatePool = getattr(self, self.sel_parents)()
				Parents, Offspring = self.advanceGeneration(MatePool, tsp_prob_cross, kp_prob_cross, tsp_prob_mut,
				                                            kp_prob_mut)

				self.Population = getattr(self, self.sel_survivors)(Offspring)

				if self.plots['popDiversity'] == True:
					diversityPop = self.evalDiversity()
					diver.append(diversityPop[0])
					maxDiver.append(diversityPop[1])

				if self.Hypermutation['activate']:
					if self.emigrants['active']:
						self.Population = self.immigration(self.emigrants['sizePerct'])
						self._evalPopulation()

				# self._evalPopulation() -->  isto n deve ser necessario uma vez que todos os items sao avaliados quando postos na lista

				self.StatBest[_run].append(self._getPopulationBest()[1])
				self.StatAvg[_run].append(self._getPopulationAverage())

			avg = sum(self.StatBest[_run]) / len(self.StatBest[_run])
			print('-- Average Best: ' + str(avg))
			print('---Best in run: ' + "%.2f" % max(self.StatBest[_run]))
			print('')

			if self.plots['popDiversity'] == True:
				self.plotDiversity(diver, maxDiver)

		StatGener = list(zip(*self.StatBest))
		_func = max if self._reverseOrder() else min

		self.StatBestByRun = [_func(GenerStats) for GenerStats in StatGener]
		self.StatAvgBestByRun = [sum(GenerStats) / len(GenerStats) for GenerStats in StatGener]
		self.StatStdDevBestByRun = [
			np.sqrt(
				sum([(best_val - self.StatAvgBestByRun[generation]) ** 2 for best_val in GenerStats]) / len(GenerStats))
			for generation, GenerStats in enumerate(StatGener)]


		self.printTime()
		t.cancel()
		self.writeToFile()

	def advanceGeneration(self, MatePool, tsp_prob_cross, kp_prob_cross, tsp_prob_mut, kp_prob_mut):
		size_pop = len(self.Population)
		Parents = []
		for j in range(0, size_pop - 1, 2):
			Indiv1 = pickle.loads(pickle.dumps(MatePool[j]))
			Indiv2 = pickle.loads(pickle.dumps(MatePool[j + 1]))

			Indiv1[0][0], Indiv2[0][0] = self.TSPConfig['recombination'](Indiv1[0][0], Indiv2[0][0],
			                                                             tsp_prob_cross)
			Indiv1[0][1], Indiv2[0][1] = self.KPConfig['recombination'](Indiv1[0][1], Indiv2[0][1],
			                                                            kp_prob_cross)

			Parents.append(Indiv1)
			Parents.append(Indiv2)

		Offspring = []
		for Indiv in Parents:
			_Indiv = pickle.loads(pickle.dumps(Indiv))
			_Indiv[0][0] = self.TSPConfig['mutation'](_Indiv[0][0], tsp_prob_mut)
			_Indiv[0][1] = self.KPConfig['mutation'](_Indiv[0][1], kp_prob_mut)

			_Indiv[1] = self.fitness_func(_Indiv[0])

			if self.KPConfig['local_search'] != None:
				_Indiv = self.KPConfig['local_search'](_Indiv)

			if random() < self.KPConfig['prob_heur']:
				_Indiv = self.delayPacking(_Indiv)

			Offspring.append(_Indiv)
		return Parents, Offspring

	def plotDiversity(self, diver, maxDiver):
		timestamp = time.gmtime()
		timestamp = '' + str(timestamp.tm_mday) + '_' + str(timestamp.tm_hour) + '_' + str(timestamp.tm_min)

		fileName = str(self.oProblem.numCities) + "_" + str(self.oProblem.numItems) + "_" + str(
			self.oProblem.instance) + "_" + str(
			self.oProblem.tight) + "_" + timestamp
		path = 'Results/'
		plt.plot([x for x in range(len(diver))], diver)
		plt.plot([x for x in range(len(diver))], maxDiver)
		plt.xlabel('Geracoes')
		plt.ylabel('Entropia de Shannon')
		plt.title('Variação da diversidade ao longo das gerações')
		plt.legend(loc='best')

		plt.legend(loc='upper right')
		plt.savefig(path + fileName)

	def evalDiversity(self):
		equalInd = []
		individuos = [x[0] for x in self.Population]
		items = [x[1] for x in individuos]
		paths = [x[0] for x in individuos]

		for i in range(len(individuos)):
			for j in range(i, len(individuos)):
				# Diferencas de items
				diferencasItem = 0
				for z in items[i]:
					if z not in items[j]:
						diferencasItem += 1

				difPath = 0
				for z in range(len(paths[i])):
					if paths[i][z] != paths[j][z]:
						difPath += 1
				if diferencasItem == 0 and difPath == 0 and i != j:
					equalInd.append((i, j))

		if len(equalInd) == 0:
			return (np.log2(len(self.Population)), np.log2(len(self.Population)))
		else:

			unique, counts = np.unique([x[0] for x in equalInd], return_counts=True)
			counts += 1

			pop_t = len(self.Population)
			entro = 0
			for i in counts:
				pk = i / pop_t
				entro += pk * np.log2(pk)

			for i in range(pop_t - len(counts)):
				pk = 1 / pop_t
				entro += pk * np.log2(pk)

			return (-entro, np.log2(pop_t - len(counts)))

	def writeToFile(self):
		timestamp = time.gmtime()
		timestamp = '' + str(timestamp.tm_mday) + '_' + str(timestamp.tm_hour) + '_' + str(timestamp.tm_min)

		fileName = str(self.oProblem.numCities) + "_" + str(self.oProblem.numItems) + "_" + str(
			self.oProblem.instance) + "_" + str(
			self.oProblem.tight) + "_" + timestamp

		path = 'Results/'
		f = open(path + fileName + ".txt", 'w')

		jStatBest = json.dumps({'StatBest': self.StatBest})
		jStatAvg = json.dumps({'StatAvg': self.StatAvg})
		jStatBestByRun = json.dumps({'StatBestByRun': self.StatBestByRun})
		jStatAvgByRun = json.dumps({'StatAvgByRun': self.StatAvgBestByRun})
		jStatStdDev = json.dumps({'StatStdDev': self.StatStdDevBestByRun})

		f.write(jStatBest + "\n" +
		        jStatAvg + "\n" +
		        jStatBestByRun + "\n" +
		        jStatAvgByRun + "\n" +
		        jStatStdDev + "\n")

		f.close()

	@staticmethod
	def repairKP(Problem, cromo):
		_cromo = cromo[:]
		_cromo = [*set(_cromo)]
		_cromo.sort()

		ItemRatio = []

		total_weight = 0
		for i in _cromo:
			item = i % Problem.numItems
			total_weight += Problem.items[item].weight
			ItemRatio.append(
				[i, Problem.items[item].weight, float(Problem.items[item].value / Problem.items[item].weight)])

		ItemRatio.sort(key=itemgetter(2))

		for item, weight, ratio in ItemRatio:
			if total_weight <= Problem.knapsackWeight:
				return _cromo
			else:
				total_weight -= weight
				del _cromo[_cromo.index(item)]

		return _cromo

	@staticmethod
	def standardFitnessWrapper(Problem):
		def standardFitness(Indiv):
			Cities = Indiv[0]
			Items = Indiv[1]

			FullRoute = np.append(Cities, Cities[0])

			g = 0
			total_time = 0
			carrying_weight = 0
			speed_coef = (Problem.vmax - Problem.vmin) / Problem.knapsackWeight

			for i, city in enumerate(FullRoute):
				if i + 1 == len(FullRoute):
					continue

				_index_start = Problem.numItems * city
				for j in range(Problem.numItems):
					if (_index_start + j) in Items:
						Item = Problem.items[j]
						g += Item.value
						carrying_weight += Item.weight

				cur_speed = Problem.vmax - carrying_weight * speed_coef

				if cur_speed < Problem.vmin:
					print('Invalid Solution Found! Current speed is only negative with infeasible solutions!')
					cur_speed = Problem.vmin

				cur_city = FullRoute[i]
				next_city = FullRoute[i + 1]
				dist = Problem.dists[cur_city][next_city]
				total_time += dist / cur_speed

			fitness_value = g - Problem.knapsackRent * total_time

			return fitness_value

		return standardFitness