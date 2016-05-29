from Operators.IntegerOperators import *
from Operators.LocalSearchOperators import *
from Problem.ProblemRepresentation import *
from Utils.File import *

from Display.Visual import *

if __name__ == '__main__':
    Recombinations = [{'name': 'PMX', 'operator': IntegerOperators.cross_pmx, 'display': 'PMX'},
                      {'name': 'OX', 'operator': IntegerOperators.cross_order, 'display': 'OX'}]

    Problems = []

    '''
    Problem = {}
    Problem['name'] = 'tsp'
    TSPCoord = ProblemRepresentation.readTSPCoord('Data/TSP/wi29.tsp')
    TSPDetails = ProblemRepresentation.parseTSPCoord(TSPCoord)
    Problem['config'] = {'name': Problem['name'], 'TSPDetails': TSPDetails, 'cromo_size': len(TSPDetails),
                         'optimization': Algorithm.Minimization}
    Problem['generate_pop'] = ProblemRepresentation.generateTSPPopulation
    Problem['fitness'] = ProblemRepresentation.standardFitnessTSP
    Problems.append(Problem)
    '''

    '''
    Problem = {}
    Problem['name'] = 'n_queens'
    Problem['config'] = {'name': Problem['name'], 'cromo_size': 8, 'optimization': Algorithm.Minimization}
    Problem['generate_pop'] = ProblemRepresentation.generateTSPPopulation
    Problem['fitness'] = ProblemRepresentation.standardFitnessNQueens
    Problems.append(Problem)
    '''

    for Recombination in Recombinations:
        for Problem in Problems:
            Config = Problem['config']
            Config['numb_generations'] = 100
            Config['pop_size'] = 100
            Config['runs'] = 30
            Config['tournament_size'] = int(Config['pop_size'] / 5)
            Config['sel_parents'] = 'tournament'
            Config['sel_survivors'] = 'elitism'
            Config['elite_percent'] = 0.1
            Config['generate_pop'] = Problem['generate_pop']
            Config['fitness_func'] = Problem['fitness']

            Config['prob_cross'] = 0.9
            Config['prob_mut'] = 0.1
            Config['recombination'] = Recombination['operator']
            Config['mutation'] = IntegerOperators.mut_insert

            Plots = {}
            Plots['pop_diversity'] = False

            print('Problem: ' + str(Problem['name']))
            oAlgorithm = Algorithm(Config, Plots)
            oAlgorithm.run()

            _func = max if oAlgorithm._reverseOrder() else min
            BestOfAll = "%.2f" % _func(oAlgorithm.StatBestByRun)
            print('## Best of All: ' + BestOfAll)

            timestamp = time.gmtime()
            timestamp = '' + str(timestamp.tm_mday) + '_' + str(timestamp.tm_hour) + '_' + str(timestamp.tm_min)

            plt_name = Problem['name'] + "_" + \
                       Recombination['name'] + "_" + \
                       str(Problem['config']['cromo_size']) + "_" + \
                       timestamp

            Visual.plotBestAverage(oAlgorithm.StatBestByRun, oAlgorithm.StatAvgBestByRun, store='store',
                                   figure_legend=plt_name)
            File.writeToFile(Config, Recombination, Problem, oAlgorithm.StatBestByRun, oAlgorithm.StatAvgBestByRun)

            print('')
