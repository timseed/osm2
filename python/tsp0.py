import logging
from itertools import combinations
from math import sqrt
from pprint import pprint

import daiquiri
import mlrose
import simplekml

logging.basicConfig(level=logging.DEBUG)
logger = daiquiri.getLogger(__name__)
logger.debug("Test")

from utils import get_data, Province

cnt = -1


def idx():
    global cnt
    cnt += 1
    return cnt


def dist(pos1: Province, pos2: Province) -> float:
    yDis = abs(int(Hours_to_km(pos1.lat)) - int(Hours_to_km(pos2.lat)))
    xDis = abs(int(Hours_to_km(pos2.lon)) - int(Hours_to_km(pos2.lon)))
    distance = sqrt((xDis * xDis) + (yDis * yDis))
    return distance


def Hours_to_km(decimal_hours):
    """
    14.234 is 14*60 + .234 * 60 Miles
    :param decimal_hours:
    :return:
    """
    return decimal_hours * 60.0 * 1.56


luzon_province_capitals = get_data()[:10]
# Reindex the ID's
for n in luzon_province_capitals:
    n.id = idx()

pprint(luzon_province_capitals)
dist_pairs = list(combinations([n.id for n in luzon_province_capitals], 2))
pprint(dist_pairs)
#
# Using is index  - calculate the distance between each pair.
#
#
#
coords_list = [(n.lon, n.lat) for n in luzon_province_capitals]
dist_list = []
for n in dist_pairs:
    frm = luzon_province_capitals[n[0]]
    too = luzon_province_capitals[n[1]]
    dist_list.append((frm, too, dist(frm,too)))
pprint(dist_list)

# Initialize fitness function object using coords_list
fitness_coords = mlrose.TravellingSales(coords=coords_list)
# Initialize fitness function object using dist_list
#fitness_dists = mlrose.TravellingSales(distances=dist_list)
problem_fit = mlrose.TSPOpt(length=len(coords_list), fitness_fn=fitness_coords,
                            maximize=False)
problem_no_fit = mlrose.TSPOpt(length=len(coords_list), coords=coords_list,
                               maximize=False)
# Solve problem using the genetic algorithm
best_state, best_fitness = mlrose.genetic_alg(problem_fit,pop_size=1000, random_state=2, max_attempts=1000,max_iters=100)

print('The best state found is: ', best_state)
kml = simplekml.Kml()
kml_route = simplekml.Kml()
route = []
cnt = 0
for n in best_state:
    print(f"{luzon_province_capitals[n].state} {luzon_province_capitals[n].name}")
    kml.newpoint(name=str(cnt) + " " + luzon_province_capitals[n].state + " " + luzon_province_capitals[n].name,
                 coords=[(luzon_province_capitals[n].lon, luzon_province_capitals[n].lat)])
    route.append((luzon_province_capitals[n].lon, luzon_province_capitals[n].lat))
    cnt += 1
kml.save("route.kml")

lin = kml_route.newlinestring(name="Luzon1", description="Shortest Path around Luzon",
                              coords=route)
lin.style.linestyle.color = 'de0000ff'  # Red
lin.style.linestyle.width = 5  # 10 pixels
kml_route.save("way.kml")
print('The fitness at the best state is: ', best_fitness)
