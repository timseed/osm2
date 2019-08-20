import psycopg2
import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations
from collections import Counter
from math import sqrt
from itertools import combinations
from pprint import pprint


def distance(lng1,lat1,lng2,lat2):
    # All distances are in Units of 60
    x_dist = abs(lng1-lng2)
    y_dist = abs(lat1-lat2)
    return sqrt(abs((x_dist*x_dist) -(y_dist*y_dist))) *60.0

def get_data():
    rv = [] 
    conn = psycopg2.connect(
        host='0.0.0.0',
        port=54320,
        dbname='gis',
        user='postgres',
    )
    cur = conn.cursor()
    luzon_capital = """
    select  pt.osm_id,
       pt.tags->'is_in:state' as state,
       pt.name as name,ST_X(ST_TRANSFORM(pt.way,4674)) AS LONG,
       ST_Y(ST_TRANSFORM(pt.way,4674)) AS LAT from planet_osm_point pt ,
       planet_osm_polygon poly
       where defined(pt.tags,'capital') and  
       defined(pt.tags,'is_in:state') and  
       poly.name='Luzon' and
      ST_Contains(poly.way, pt.way)
        order by name;
    """
    cur.execute(luzon_capital)
    for row in cur:
        print(row)
        rv.append(row)

    conn.commit()
    cur.close()
    conn.close()
    return rv

a=get_data()
pprint(a)
G=nx.DiGraph()
for n in a: 
  print(f"Adding {n[1]} {n[2]} ") 
  G.add_node(n[2],POS=(n[3],n[4]))

node_ids =[ nid for nid in range(len(a))]
points = list(combinations(node_ids,2))
pprint(points)

#print(f"distance {d}")

