from random import *

class FloatOperators:
    @staticmethod
    def muta_float(cromo,prob_muta):
        # Mutation by gene
        _cromo = cromo[:]
        for i in range(len(cromo)):
            _cromo[i] = FloatOperators.muta_float_gene(_cromo[i],prob_muta)
        return _cromo
    
    @staticmethod
    def muta_float_gene(gene, prob_muta):
        g = gene
        if random() < prob_muta:
            g += np.random.normal()
        return g
    
    @staticmethod
    def float_cross(cromo_1, cromo_2,prob_cross):
        alpha = 0.6
        if random() < prob_cross:
            f1=[]
            f2=[]
            for i in range(0,len(cromo_1)):
                x1 = alpha * cromo_1[i] + (1-alpha) * cromo_2[i]
                x2 = alpha * cromo_2[i] + (1-alpha) * cromo_1[i]
                f1.append(x1)
                f2.append(x2)
            return f1,f2
        else:
            return cromo_1,cromo_2
