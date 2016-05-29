import json
import pickle
import threading
import time
from operator import *
from random import *

import matplotlib

from Problem.ProblemRepresentation import *
from Individual.population import *

#matplotlib.use('Agg')
import matplotlib.pyplot as plt

#plt.style.use('ggplot')
import numpy as np


class Algorithm:
    Maximization = 'maximize'
    Minimization = 'minimize'

    def __init__(self, Config, Plots):

        self.Config = Config
        self.runs = Config['runs']
        self.numb_generations = Config['numb_generations']
        self.tournament_size = Config['tournament_size']

        self.sel_parents = Config['sel_parents']
        self.sel_survivors = Config['sel_survivors']
        self.elite_percent = Config['elite_percent']
        self.fitness_func = Config['fitness_func']

        self.optimization = Config['optimization'] if 'optimization' in Config.keys() else Algorithm.Maximization
        self.size_pop = Config['pop_size']

        self.recombination = Config['recombination']
        self.prob_cross = Config['prob_cross']

        self.mutation = Config['mutation']
        self.prob_mut = Config['prob_mut']

        self.StatBest = []
        self.StatAvg = []
        self.Plots = Plots

    def _initializePop(self):
        self.Population = self.Config['generate_pop'](self.Config)

    def _reverseOrder(self):
        return True if self.optimization == Algorithm.Maximization else False

    def _evalPopulation(self):
        self.Population = [[Indiv[0], self.fitness_func(self.Config, Indiv[0])] for Indiv in self.Population]

    def _getPopulationAverage(self):
        return sum([fit for cromo, fit in self.Population]) / len(self.Population)

    def _getPopulationBest(self):
        _Population = self.Population
        _Population.sort(key=itemgetter(1), reverse=self._reverseOrder())
        return _Population[0]

    def tournament(self):
        MatePool = []
        _reverse = self._reverseOrder()
        for i in range(self.size_pop):
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

        self.TimeRun = []
        self.BestRun = []

        for _run in range(self.runs):
            self._initializePop()
            print('Starting Run: ' + str(_run + 1))

            self._evalPopulation()

            self.StatBest[_run] = [self._getPopulationBest()[1]]
            self.StatAvg[_run] = [self._getPopulationAverage()]

            Diversity = []
            MaxDiver = []

            start_time = time.time()
            for i in range(self.numb_generations):
                if (i + 1) % 20 == 0:
                    print('--Generation ' + str(i + 1))
                # print(str(i) + ' ' + str(self.StatBest[_run][-1]))

                MatePool = getattr(self, self.sel_parents)()

                Parents = []
                for j in range(0, self.size_pop - 1, 2):
                    Indiv1 = pickle.loads(pickle.dumps(MatePool[j]))
                    Indiv2 = pickle.loads(pickle.dumps(MatePool[j + 1]))
                    Indiv1[0], Indiv2[0] = self.recombination(Indiv1[0], Indiv2[0], self.prob_cross)
                    Parents.append(Indiv1)
                    Parents.append(Indiv2)

                Offspring = []
                for Indiv in Parents:
                    _Indiv = pickle.loads(pickle.dumps(Indiv))
                    _Indiv[0] = self.mutation(_Indiv[0], self.prob_mut)
                    _Indiv[1] = self.fitness_func(self.Config, _Indiv[0])
                    Offspring.append(_Indiv)

                self.Population = getattr(self, self.sel_survivors)(Offspring)

                if self.Plots['pop_diversity'] == True:
                    DiversityPop = self.evalDiversity()
                    Diversity.append(DiversityPop[0])
                    MaxDiver.append(DiversityPop[1])

                self.StatBest[_run].append(self._getPopulationBest()[1])
                self.StatAvg[_run].append(self._getPopulationAverage())


            final_time = time.time()

            avg = sum(self.StatBest[_run]) / len(self.StatBest[_run])
            print(self._getPopulationBest()[0])
            print('-- Time: ' + str(final_time - start_time))
            print('-- Average Best: ' + str(avg))
            _func = max if self._reverseOrder() else min
            print('---Best in run: ' + "%.2f" % _func(self.StatBest[_run]))

            self.TimeRun.append(final_time - start_time)
            self.BestRun.append(_func(self.StatBest[_run]))

            print('')

            if self.Plots['pop_diversity'] == True:
                self.plotDiversity(Diversity, MaxDiver)

        StatGener = list(zip(*self.StatBest))
        _func = max if self._reverseOrder() else min

        self.StatBestByRun = [_func(GenerStats) for GenerStats in StatGener]
        self.StatAvgBestByRun = [sum(GenerStats) / len(GenerStats) for GenerStats in StatGener]
        self.StatStdDevBestByRun = [np.sqrt(
            sum([(best_val - self.StatAvgBestByRun[generation]) ** 2 for best_val in GenerStats]) / len(GenerStats)) for
                                    generation, GenerStats in enumerate(StatGener)]

        self.printTime()
        t.cancel()
        #self.writeToFile()

    def plotDiversity(self, Diversity, MaxDiver):
        timestamp = time.gmtime()
        timestamp = '' + str(timestamp.tm_mday) + '_' + str(timestamp.tm_hour) + '_' + str(timestamp.tm_min)

        filename = self.Config['name'] + "_" + timestamp
        path = 'Results/'
        plt.plot([x for x in range(len(Diversity))], Diversity)
        plt.plot([x for x in range(len(Diversity))], MaxDiver)
        plt.xlabel('Geracoes')
        plt.ylabel('Entropia de Shannon')
        plt.title('Variação da diversidade ao longo das gerações')
        plt.savefig(path + filename)

    def evalDiversity(self):
        EqualIndiv = []
        Individs = [x[0] for x in self.Population]

        for i in range(len(Individs)):
            for j in range(i, len(Individs)):
                dif_path = 0
                for z in range(len(Individs[i])):
                    if Individs[i][z] != Individs[j][z]:
                        dif_path += 1
                if dif_path == 0 and i != j:
                    EqualIndiv.append((i, j))

        if len(EqualIndiv) == 0:
            return (np.log2(len(self.Population)), np.log2(len(self.Population)))
        else:
            unique, counts = np.unique([x[0] for x in EqualIndiv], return_counts=True)
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
        filename = self.Config['name'] + "_" + timestamp

        path = 'Results/'
        f = open(path + filename + ".txt", 'w')

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
