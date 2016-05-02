from random import *

class BinaryOperators:
    @staticmethod
    def muta_bin(cromo, prob_muta):
        # Mutation by gene
        _cromo = cromo[:]
        for i in range(len(cromo)):
            _cromo[i] = BinaryOperators.muta_bin_gene(_cromo[i],prob_muta)
        return _cromo
    
    @staticmethod
    def muta_bin_gene(gene, prob_muta):
        g = gene
        if random() < prob_muta:
            g ^= 1
        return g

    @staticmethod
    def one_point_cross(cromo_1, cromo_2, prob_cross):
        if random() < prob_cross:
            pos = randint(0,len(cromo_1))
            f1 = cromo_1[0:pos] + cromo_2[pos:]
            f2 = cromo_2[0:pos] + cromo_1[pos:]
            return f1,f2
        else:
            return cromo_1,cromo_2

    @staticmethod
    def two_points_cross(cromo_1, cromo_2, prob_cross):
        if random() < prob_cross:
            pc = sample(range(len(cromo_1)),2)
            pc.sort()
            pc1,pc2 = pc
            f1 = cromo_1[:pc1] + cromo_2[pc1:pc2] + cromo_1[pc2:]
            f2 = cromo_2[:pc1] + cromo_1[pc1:pc2] + cromo_2[pc2:]
            return f1,f2
        else:
            return cromo_1,cromo_2

    @staticmethod
    def uniform_cross(cromo_1, cromo_2, prob_cross):
        if random() < prob_cross:
            f1 = []
            f2 = []
            for i in range(0,len(cromo_1)):
                if random() < 0.5:
                    f1.append(cromo_1[i])
                    f2.append(cromo_2[i])
                else:
                    f1.append(cromo_2[i])
                    f2.append(cromo_1[i])
            return f1,f2
        else:
            return cromo_1,cromo_2