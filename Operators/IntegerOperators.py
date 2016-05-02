import random
import numpy as np
from Problem.Algorithm import *

class IntegerOperators:
    
    @staticmethod
    # Variation operators: swap mutation
    def mut_swap(cromo, prob_muta):
        if random.random() < prob_muta:
            comp = len(cromo) - 1
            copia = cromo[:]
            i = randint(0, comp)
            j = randint(0, comp)
            while i == j:
                i = randint(0, comp)
                j = randint(0, comp)
            copia[i], copia[j] = copia[j], copia[i]
            return copia
        else:
            return cromo
 
    @staticmethod
    # Variation operators: insert selection
    def mut_insert(cromo, prob_muta):
        if random.random() < prob_muta:
            comp = len(cromo) - 1
            copia = cromo[:]
            i = randint(0, comp)
            j = randint(0, comp)
            while abs(i - j) < 2:
                i = randint(0, comp)
                j = randint(0, comp)
            if j < i:
                temp = i
                i=j
                j=temp
            pos_insercao = (i+1)% (len(copia)-1)
            temp = copia[j]
            copia.remove(copia[j])
            copia.insert(pos_insercao,temp)
            return copia
        else:
            return cromo
        
    @staticmethod
    # Variation operators: scramble mutation
    def mut_scramble(cromo,prob_muta):
        if random.random() < prob_muta:
            comp = len(cromo)-1
            copia = cromo[:]
            i = randint(0,comp)
            j = randint(0,comp)
            while (i == j) or (j > i):
                i = randint(0,comp)
                j = randint(0,comp)

            shuffle(copia[i:j])
            return copia
        else:
            return cromo
        
    @staticmethod
    # Variation Operators :  Cycle Cross
    def cross_cycle(cromo_1,cromo_2,prob_cross):
        if random.random() < prob_cross:
            size = len(cromo_1)
            f1 = [None]*size
            f2 = [None]*size
            Cycles = []
            for i in range(size):
                cycles_count = len(Cycles)
                if any(i in Cycle for Cycle in Cycles):
                    continue

                Cycle = []
                index = i
                while index not in Cycle:
                    Cycle.append(index)
                    if cycles_count%2==0:
                        f1[index] = cromo_1[index]
                        f2[index] = cromo_2[index]
                    else:
                        f1[index] = cromo_2[index]
                        f2[index] = cromo_1[index]
                        
                    index = cromo_1.index(cromo_2[index])
                Cycles.append(Cycle)

            return f1,f2
        else:
            return cromo_1,cromo_2

    @staticmethod
    # Variation Operators :  PMX
    def cross_pmx(cromo_1,cromo_2,prob_cross):
        if random.random() < prob_cross:
            size = len(cromo_1)
            pc = sample(range(size),2)
            pc.sort()
            pc1,pc2 = pc

            f1 = IntegerOperators._apply_pmx_cross(cromo_1,cromo_2,pc1,pc2)
            f2 = IntegerOperators._apply_pmx_cross(cromo_2,cromo_1,pc1,pc2)
        
            return f1,f2
        else:
            return cromo_1,cromo_2

    def _apply_pmx_cross(cromo_master,cromo_slave,pc1,pc2):
        size = len(cromo_master)
        f = [None] * size
        f[pc1:pc2+1] = cromo_master[pc1:pc2+1]

        pos = pc1
        while pos <= pc2:
            source_index = cromo_master.index(cromo_slave[pos])
            if source_index>=pc1 and source_index<=pc2:
                pos += 1
                continue

            val = cromo_master[pos]
            index = cromo_slave.index(val)
            while index>=pc1 and index<=pc2:
                val = cromo_master[index]
                index = cromo_slave.index(val)

            f[index] = cromo_slave[pos]
            pos += 1

        pos = (pc2+1) % size
        while pos != pc1:
            if f[pos] != None: 
                pos = (pos + 1)% size	
                continue

            f[pos] = cromo_slave[pos]
            pos = (pos + 1) % size		

        return f
    
    @staticmethod
    # Variation Operators :  OX - order crossover
    def cross_order(cromo_1,cromo_2,prob_cross):
        size = len(cromo_1)
        if random.random() < prob_cross:
            pc= sample(range(size),2)
            pc.sort()
            pc1,pc2 = pc
            
            f1 = [None] * size
            f2 = [None] * size
            
            f1[pc1:pc2+1] = cromo_1[pc1:pc2+1]
            f2[pc1:pc2+1] = cromo_2[pc1:pc2+1]
            
            pos = (pc2+1)% size
            fixed = pos
            
            while pos != pc1:
                j = fixed % size
                while cromo_2[j] in f1:
                    j = (j+1) % size	
                f1[pos] = cromo_2[j]
                pos = (pos + 1)% size		

            pos = (pc2+1)% size
            while pos != pc1:
                j = fixed % size
                while cromo_1[j] in f2:
                    j = (j+1) % size	
                f2[pos] = cromo_1[j]
                pos = (pos + 1)% size	
            return f1,f2
        else:
            return cromo_1,cromo_2
    
    # TODO: implementar outros operadores crossover para testes

    @staticmethod
    # Variation Operators :  Translocation
    def cross_translocation_wrapper(Problem):
        def cross_translocation(cromo_1,cromo_2,prob_cross):
            if len(cromo_1)>2 and len(cromo_2)>2 and random.random() < prob_cross:
                pc1 = sample(range(len(cromo_1)),2)
                pc1.sort()
                pc11,pc12 = pc1

                pc2 = sample(range(len(cromo_2)),2)
                pc2.sort()
                pc21,pc22 = pc2
            
                f1 = cromo_1[:pc11] + cromo_2[pc21:pc22] + cromo_1[pc12:]
                f2 = cromo_2[:pc21] + cromo_1[pc11:pc12] + cromo_2[pc22:]
            
                f1 = Algorithm.repairKP(Problem,f1)
                f2 = Algorithm.repairKP(Problem,f2)

                return f1,f2
            else:
                return cromo_1,cromo_2
        return cross_translocation
    
    @staticmethod
    # Variation operators: integer gene mutation
    def mut_ttp_kp_int_wrapper(Problem):
        def mut_ttp_kp_int(cromo, prob_muta):
            _cromo = cromo[:]
            
            min_val = 0 if len(cromo)>1 else 1
            for i in range(len(cromo)):
                if i >= len(_cromo):
                    break

                _action = rand.randint(min_val, 2)
                if random.random() < prob_muta:
                    if _action==0:
                        del _cromo[rand.randint(0, len(_cromo)-1)]
                    else:
                        _rand_item = rand.randint(0,Problem.numItems-1)
                        _cities = [_city for _city, available in enumerate(Problem.available[_rand_item]) if available==True and _city * Problem.numItems + _rand_item not in _cromo]
                        if len(_cities)>0:
                            _rand_city = sample(_cities,1)[0]
                            _item = _rand_city * Problem.numItems + _rand_item
                            if _action==1:
                                _cromo.append(_item)
                            else:
                                _cromo[i] = _item
                                
            _cromo = Algorithm.repairKP(Problem,_cromo)

            return _cromo
        return mut_ttp_kp_int
    