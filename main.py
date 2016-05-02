from Operators.IntegerOperators import *
from Operators.LocalSearchOperators import *
from Problem.problem import ProblemRepresentation

if __name__ == '__main__':
    Configs = []

    for Config in Configs:

        print('Cities: ' + str(Config['n_cities']) + ' Items: ' + str(Config['n_items']) + ' Instance: ' + str(Config['instance']) + ' Thighness: ' + str(Config['thighness']))
        oProblem = ProblemRepresentation(Config['n_cities'], Config['n_items'], Config['instance'], Config['thighness'])

        pop_size = 20
        numb_generations = 20

        runs = 3
        tournament_size = int(pop_size/5)
    
        sel_parents = 'tournament'
        sel_survivors = 'elitism'
        elite_percent = 0.1
        fitness_func = Algorithm.standardFitnessWrapper(oProblem)

        Hypermutation = {}
        Hypermutation['generations'] = int(numb_generations/20)
        Hypermutation['max_generations'] = int(pop_size/10)
        Hypermutation['activate'] = True

        TSPConfig = {}
        TSPConfig['prob_cross'] = [0.9, 0.55]
        TSPConfig['prob_mut'] = [0.1, 0.55]
        TSPConfig['prob_hmut'] = 0.6
        TSPConfig['recombination'] = IntegerOperators.cross_pmx
        TSPConfig['mutation'] = IntegerOperators.mut_insert
        TSPConfig['prob_variation_cross'] = True
        TSPConfig['prob_variation_mut'] = True

        KPConfig = {}
        KPConfig['prob_cross'] = [0.25, 0.3]
        KPConfig['prob_mut'] = [0.05, 0.1]
        KPConfig['prob_hmut'] = 0.25 # ou 0.2
        KPConfig['prob_heur'] = 0.9
        KPConfig['recombination'] = IntegerOperators.cross_translocation_wrapper(oProblem)
        KPConfig['mutation'] = IntegerOperators.mut_ttp_kp_int_wrapper(oProblem)
        KPConfig['local_search'] = LocalSearchOperators.kp_hillclimbing_wrapper(oProblem,fitness_func,Config['n_cities']*Config['n_items'] if Config['n_cities']*Config['n_items'] < 1000 else 1000)
        KPConfig['prob_variation_cross'] = True
        KPConfig['prob_variation_mut'] = True

        plots = {}
        plots['popDiversity'] = True

        emigrants = {}
        emigrants['sizePerct'] = 0.3
        emigrants['active'] = True

        oAlgorithm = Algorithm(oProblem, runs, numb_generations, tournament_size, sel_parents,
                               sel_survivors, elite_percent, fitness_func, TSPConfig, KPConfig, Hypermutation, plots,
                               pop_size, emigrants)
        oAlgorithm.run()
        
        BestOfAll = "%.2f" % max(oAlgorithm.StatBestByRun) 
        print('## Best of All: ' + BestOfAll)

        #Visual.plotBestAverage(oAlgorithm.StatBestByRun,oAlgorithm.StatAvgBestByRun)
        print('')