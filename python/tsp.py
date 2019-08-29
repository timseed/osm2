import logging
from itertools import combinations
from math import hypot
from pprint import pprint

import daiquiri
import mlrose
import simplekml

logging.basicConfig(level=logging.DEBUG)
logger = daiquiri.getLogger(__name__)
logger.debug("Test")

from utils import get_data

cnt = -1


def idx():
    global cnt
    cnt += 1
    return cnt

def Hours_to_km(decimal_hours):
    """
    14.234 is 14*60 + .234 * 60 Miles
    :param decimal_hours:
    :return:
    """
    return decimal_hours*60.0*1.56


luzon_province_capitals = get_data()
#Reindex the ID's
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
coords_list = [(n.lon,n.lat) for n in luzon_province_capitals]
dist_list = []
for n in dist_pairs:
    frm = n[0]
    too = n[1]
    dist_in_km =             hypot(Hours_to_km(luzon_province_capitals[frm].lat) -
                                   (luzon_province_capitals[too].lat),
                                   (luzon_province_capitals[frm].lon) -
                                   (luzon_province_capitals[too].lon))
    dist_list.append((frm, too, dist_in_km))
pprint(dist_list)



# Initialize fitness function object using coords_list
fitness_coords = mlrose.TravellingSales(coords=coords_list)
# Initialize fitness function object using dist_list
fitness_dists = mlrose.TravellingSales(distances=dist_list)
problem_fit = mlrose.TSPOpt(length=len(coords_list), fitness_fn=fitness_coords,
                            maximize=False)
problem_no_fit = mlrose.TSPOpt(length=len(coords_list), coords=coords_list,
                               maximize=False)
# Solve problem using the genetic algorithm
best_state, best_fitness = mlrose.genetic_alg(problem_fit, random_state=2)

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
