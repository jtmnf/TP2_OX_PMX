import random as rand
import numpy as np
from Problem.Algorithm import *

class LocalSearchOperators:
    
    @staticmethod
    def kp_hillclimbing_wrapper(Problem,fitness_func,max_iterations):
        def kp_hillclimbing(Indiv):
            return Indiv
            for i in range(max_iterations):
                _Indiv = copy.deepcopy(Indiv)
                if len(_Indiv[0][1])==0:
                    continue

                _index = rand.randint(0,len(_Indiv[0][1])-1)
                _rand_item = rand.randint(0,Problem.numItems-1)
                _cities = [_city for _city, available in enumerate(Problem.available[_rand_item]) if available==True and _city * Problem.numItems + _rand_item not in _Indiv[0][1] and _rand_item!=_Indiv[0][1][_index]]
                if len(_cities)>0:
                    _rand_city = sample(_cities,1)[0]
                    _Indiv[0][1][_index] = _rand_city * Problem.numItems + _rand_item
                    _Indiv[0][1] = Algorithm.repairKP(Problem,_Indiv[0][1])

                    fitness = fitness_func(_Indiv[0])
                    if fitness > _Indiv[1]:
                        _Indiv[1] = fitness
                        return _Indiv

            return _Indiv
        return kp_hillclimbing