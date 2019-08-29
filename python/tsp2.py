import tsp
from math import sqrt
from pprint import pprint

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


luzon_province_capitals = get_data()
# Reindex the ID's
for n in luzon_province_capitals:
    n.id = idx()

mat = []
for x in range(0, len(luzon_province_capitals)):
    d1 = []
    for y in range(0, len(luzon_province_capitals)):
        kms = dist(luzon_province_capitals[x],
                   luzon_province_capitals[y])
        d1.append(kms)
    mat.append(d1)

pprint(luzon_province_capitals)
#pprint(mat)
r = range(len(mat))
# Dictionary of distance
dist = {(i, j): mat[i][j] for i in r for j in r}
print(tsp.tsp(r, dist))