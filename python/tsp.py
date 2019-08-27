import logging
from itertools import combinations
from math import hypot
from pprint import pprint
import mlrose
import numpy as np
import daiquiri

logging.basicConfig(level=logging.DEBUG)
logger = daiquiri.getLogger(__name__)
logger.debug("Test")

from utils import get_data

luzon_province_capitals = get_data()
count = -1


def incr():
    global count
    count += 1
    return count


coords_list = [(incr(), a[3], a[4]) for a in luzon_province_capitals]

pprint(luzon_province_capitals)
pprint(coords_list)
dist_pairs = list(combinations([n[0] for n in coords_list], 2))
pprint(dist_pairs)
#
# Using is index  - calculate the distance between each pair.
#
#
#
dist_list = []
for n in dist_pairs:
     frm = n[0]
     too  = n[1]
     dist_in_km = 60*1.56*hypot(coords_list[frm][1]-coords_list[too][1],
                   coords_list[frm][2] - coords_list[too][2])
     dist_list.append((frm,too,dist_in_km))
pprint(dist_list)


# Initialize fitness function object using coords_list
fitness_coords = mlrose.TravellingSales(coords = coords_list)
# Initialize fitness function object using dist_list
fitness_dists = mlrose.TravellingSales(distances = dist_list)
problem_fit = mlrose.TSPOpt(length = len(coords_list), fitness_fn = fitness_coords,
                            maximize=False)
problem_no_fit = mlrose.TSPOpt(length = len(coords_list), coords = coords_list,
                               maximize=False)
# Solve problem using the genetic algorithm
best_state, best_fitness = mlrose.genetic_alg(problem_fit, random_state = 2)

print('The best state found is: ', best_state)
for n in best_state:
     print(f"{luzon_province_capitals[n][1]} {luzon_province_capitals[n][2]}")
print('The fitness at the best state is: ', best_fitness)
