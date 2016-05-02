"""
functions_2016.py
Examples for function optimizattion.
Ernesto Costa, February 2016
"""

__author__ = 'Ernesto Costa'
__date__ = 'February 2016'

import numpy as np
from sea_float_2016 import *

from Prof.utils_2016 import *


# Fitness
def merito(indiv):
	return evaluate(fenotipo(indiv))


def fenotipo(indiv):
	return indiv


def evaluate(x):
	"""Rastrigin: Rely on numpy arrays."""
	w = np.array(x)
	y = 10 * len(w) + sum((w ** 2 - 10 * np.cos(2 * np.pi * w)))
	return y

if __name__ == '__main__':
	prefix = '/Users/ernestojfcosta/tmp/'
	domain = [[-5.12, 5.12], [-5.12, 5.12], [-5.12, 5.12]]
	sigma = [0.5, 0.8, 1.0]

	# best_1 = sea_float(250, 100,domain,0.01,sigma,0.9,tour_sel(3),cross(0.3),muta_float_gaussian,sel_survivors_elite(0.1), merito)
	# display(best_1,fenotipo)

	# best_1,best,average_pop = sea_for_plot(250, 100,domain,0.01,sigma,0.9,tour_sel(3),cross(0.3),muta_float_gaussian,sel_survivors_elite(0.1), merito)
	# display_stat_1(best,average_pop)

	boa, best_average = run(5, 250, 100, domain, 0.01, sigma, 0.9, tour_sel(3), cross(0.3), muta_float_gaussian,
							sel_survivors_elite(0.1), merito)
	
    #display_stat_n(boa, best_average)
