import random as rand

import numpy as np

from Individual.abstractIndividual import AbstractInd


class Population:
    def __init__(self, problemRepresentation, popSize=20, distance=10, proportion=0.6):
        self.popSize = popSize
        self.problem = problemRepresentation
        self.pop = list()
        self.distance = distance

        self.initRandomPop(proportion)

    def initRandomIndiv(self, indiv):
        cities = [i for i in range(self.problem.numCities)]
        while len(cities) != 0:
            choice = rand.choice(cities)
            cities.remove(choice)
            indiv.cities.append(choice)

        ## Items

        # TODO: ao iniciar a populacao sempre ao maximo de carga esta se a fzer demasiada pressao ?

        # Genotipo Indiv:
        #
        # Indiv[0] = Indiv details
        # Indiv[0][0] = Indiv trip, integers list
        #   Indiv[0][1] = Indiv packing plan
        #   -Example, 4 cities, 2 items:
        #   -Cities:   0      1      2       3
        #            [0][1] [2][3] [4][5] [6][7]
        #
        #   I.E. packing plan = 1,2,5,7 means it picks item 2,1,2,2 from city 1,2,3,4 respectivly
        #   Note: the order of the cities in the packing plan is fixed, regardless of the cities trip
        #
        # Indiv[1] = fitness value

        max_load = self.problem.knapsackWeight * 1
        indiv.items = []

        init = 'rand'
        if init == 'rand':
            # TODO: find a better initialization process
            iter = 0
            max_iter_load = 10
            while iter < max_iter_load:
                iter += 1
                _rand_item = rand.randint(0, self.problem.numItems - 1)
                _cities = [_city for _city, available in enumerate(self.problem.available[_rand_item]) if
                           available == True and _city * self.problem.numItems + _rand_item not in indiv.items]
                if len(_cities) > 0:
                    _rand_item_weight = self.problem.items[_rand_item].weight
                    if indiv.weight + _rand_item_weight > max_load:
                        break
                    indiv.items.append(rand.sample(_cities, 1)[0] * self.problem.numItems + _rand_item)
                    indiv.weight += _rand_item_weight
        elif init == 'rand2':
            iter = 0
            max_iter_load = 10
            while iter < max_iter_load:
                selected = rand.randint(1, 10)
                if selected < 5:
                    break
                iter += 1
                _rand_item = rand.randint(0, self.problem.numItems - 1)
                _cities = [_city for _city, available in enumerate(self.problem.available[_rand_item]) if
                           available == True and _city * self.problem.numItems + _rand_item not in indiv.items]
                # print(_cities)
                if len(_cities) > 0:
                    _rand_item_weight = self.problem.items[_rand_item].weight
                    if indiv.weight + _rand_item_weight > max_load:
                        break
                    indiv.items.append(rand.sample(_cities, 1)[0] * self.problem.numItems + _rand_item)
                    indiv.weight += _rand_item_weight
        else:
            cities = [i for i in range(self.problem.numCities)]
            for city in reversed(indiv.cities):
                if indiv.weight < max_load:
                    _index = city * self.problem.numItems
                    for item in range(self.problem.numItems):
                        if self.problem.available[item][city]:
                            if indiv.weight + self.problem.items[item].weight < max_load:
                                selected = rand.randint(0, 1)
                                if selected == 1:
                                    indiv.items.append(_index + item)
                                    indiv.weight = indiv.weight + self.problem.items[item].weight
                            else:
                                break
                else:
                    break

        indiv.items.sort()
        return indiv

    def distanceCities(self, indiv1, indiv2):
        indivs = zip(indiv1.cities, indiv2.cities)
        distance = np.sqrt(sum([(indiv[0] - indiv[1]) ** 2 for indiv in indivs]))
        return distance

    def distanceItems(self, indiv1, indiv2):

        count = 0
        for cities in range(self.problem.numCities):
            for items in range(self.problem.numItems):
                count += (indiv1.items[cities][items] - indiv2.items[cities][items]) ** 2
        return np.sqrt(count)

    def accept(self, indiv, distance, distanceFunc):
        for individual in self.pop:
            if distance > distanceFunc(indiv, individual):
                return False
        return True

    def initRandomPop(self, proportion):
        self.pop = []
        for i in range(self.popSize):
            indiv = self.initRandomIndiv(AbstractInd())

            if self.distance != None and proportion > (i / self.popSize):
                gen_try = 0
                while not self.accept(indiv, self.distance, self.distanceCities):
                    indiv = self.initRandomIndiv(AbstractInd())
                    gen_try += 1
                    if gen_try > 4:
                        print('Too many tries for one individual')
                        break
                    else:
                        print('Trying to distribute')

            self.pop.append(indiv)

        '''
        elif proportion > (i/self.popSize):

            indiv = self.initRandomIndiv(AbstractInd())
            while not self.accept(indiv, self.distance, self.distanceItems):
                indiv = self.initRandomIndiv(AbstractInd())
                print('passou2')
            self.pop.append(indiv)
        '''

    '''
    def feasable(self, indv):

        indvSum = 0
        largestWeight = 0

        for item in indv.items:
            for itemLen in range(len(item)):
                indvSum = indvSum + item[itemLen]*self.problem.items[itemLen].weight
                if self.problem.items[itemLen].weight > largestWeight:
                    largestWeight = self.problem.items[itemLen].weight
        print(indvSum, self.problem.knapsackWeight)
        if indvSum+largestWeight > self.problem.knapsackWeight:
            indv.flagItem = False
    '''
