from itertools import combinations
from pprint import pprint

import networkx as nx

from utils import get_data

a = get_data()
pprint(a)
G = nx.DiGraph()
for n in a:
    print(f"Adding {n[1]} {n[2]} ")
    G.add_node(n[2], POS=(n[3], n[4]))

node_ids = [nid for nid in range(len(a))]
points = list(combinations(node_ids, 2))
pprint(points)

# print(f"distance {d}")
