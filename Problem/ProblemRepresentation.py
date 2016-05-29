import os.path as op
import numpy as np
import random


class ProblemRepresentation(object):
    @staticmethod
    def generateJBPopulation(Config):
        pop_size = Config['pop_size']
        dimension = Config['dimension']
        return [(ProblemRepresentation.generateJBIndivid(dimension), 0) for i in range(pop_size)]

    @staticmethod
    def generateJBIndivid(dimension):
        inf = int(0.1 * dimension)
        sup = int(0.5 * dimension)
        size = random.randint(inf, sup)
        indiv = random.sample(list(range(1, dimension + 1)), size)
        return indiv

    @staticmethod
    def generateTSPPopulation(Config):
        pop_size = Config['pop_size']
        cromo_size = Config['cromo_size']
        return [(ProblemRepresentation.generatePermIndivid(cromo_size), 0) for i in range(pop_size)]

    @staticmethod
    def generatePermIndivid(cromo_size):
        data = list(range(cromo_size))
        random.shuffle(data)
        return data

    @staticmethod
    def standardFitnessJB(Config, Indiv):
        alfa = 1.0
        beta = 3.0
        dimension = Config['dimension']

        violations = 0
        for elem in Indiv:
            limite = min(elem - 1, dimension - elem)
            vi = 0
            for j in range(1, limite + 1):
                if ((elem - j) in Indiv) and ((elem + j) in Indiv):
                    vi += 1
            violations += vi

        return alfa * len(Indiv) - beta * violations

    @staticmethod
    def standardFitnessNQueens(Config, Indiv):
        size = len(Indiv)
        # Count the number of conflicts with other queens.
        # The conflicts can only be diagonal, count on each diagonal line
        left_diagonal = [0] * (2 * size - 1)
        right_diagonal = [0] * (2 * size - 1)

        # Sum the number of queens on each diagonal:
        for i in range(size):
            left_diagonal[i + Indiv[i]] += 1
            right_diagonal[size - 1 - i + Indiv[i]] += 1

        # Count the number of conflicts on each diagonal
        violations = 0

        for i in range(2 * size - 1):
            if left_diagonal[i] > 1:
                violations += left_diagonal[i] - 1

            if right_diagonal[i] > 1:
                violations += right_diagonal[i] - 1

        return violations


    @staticmethod
    def standardFitnessTSP(Config, Indiv):
        TSPDetails = Config['TSPDetails']
        return ProblemRepresentation.evaluateStandardFitnessTSP(ProblemRepresentation.getTSPPhenotype(TSPDetails, Indiv))


    @staticmethod
    def readTSPCoord(filename):
        """ Devolve a matriz das TSPCoord a partir de filename em formato tsp."""
        with open(filename) as TSPFile:
            # read header
            linha = TSPFile.readline()
            while not linha.split()[0].isdigit():
                linha = TSPFile.readline()
            # read coordinates
            n, x, y = linha.split()
            TSPCoord = [(float(x), float(y))]
            resto = TSPFile.readlines()
            for linha in resto[:-1]:
                n, x, y = linha.split()
                TSPCoord.append((float(x), float(y)))
        return TSPCoord


    @staticmethod
    def parseTSPCoord(TSPCoord):
        """ Cria um dicionário com as cidades e suas TSPCoord."""
        TSPDetails = {}
        for i, (x, y) in enumerate(TSPCoord):
            TSPDetails[i] = (x, y)
        return TSPDetails


    @staticmethod
    def getTSPPhenotype(dicio_cidades, genotipo):
        """ Devolve o fenótipo associado."""
        fen = [dicio_cidades[cidade] for cidade in genotipo]
        return fen


    @staticmethod
    def evaluateStandardFitnessTSP(TSPPath):
        city_count = len(TSPPath)
        distance = 0
        for i in range(city_count):
            j = (i + 1) % city_count
            distance += ProblemRepresentation.getTSPDistance(TSPPath[i], TSPPath[j])
        return distance


    @staticmethod
    def getTSPDistance(cid_i, cid_j):
        """ Distância Euclidiana."""
        x_i, y_i = cid_i
        x_j, y_j = cid_j
        dx = x_i - x_j
        dy = y_i - y_j
        return np.sqrt(dx ** 2 + dy ** 2)
