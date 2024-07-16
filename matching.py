from math import log2, ceil
import networkx as nx
import numpy as np
from random import random
from scipy.spatial import Delaunay
from sys import argv

'''
Simulates the maximal matching algorithm presented in the following paper and writes information
about the run to a file so it can be visualized.

https://arxiv.org/abs/2104.09096

Author: Dominick Banasik
'''

n_est = int(argv[1])
d_est = int(argv[2])
c = int(argv[3])

name = argv[4]

out = argv[5]


# Change the following lines for different types of graphs

g: nx.Graph = nx.complete_graph(n_est)
# g: nx.Graph = nx.gnp_random_graph(100, 0.025)

points = np.random.rand(n_est, 2)
# points = list(map(lambda point: (10 * (point[0] - 0.5), 6 * (point[1] - 0.5)), points))
# g: nx.Graph = nx.Graph()

# for simplex in Delaunay(points).simplices:
#     for i in range(len(simplex)):
#         for j in range(i + 1, len(simplex)):
#             g.add_edge(simplex[i], simplex[j])

n = g.number_of_nodes()
m = g.number_of_edges()
d = g.degree

edges = map(lambda edge: f'{edge[0]} {edge[1]}\n', g.edges)
rounds = []

inactive = set()

T = c * d_est * ceil(log2(n_est))
for t in range(1, T + 1):
    r = 1 / (2 + 3 * (1 - (t - 1) / T) * d_est)
    
    sending1 = []
    listening1 = []

    for u in g.nodes:
        if u not in inactive:
            x = random()
            if x < r / 2:
                sending1.append(u)
            elif x < r:
                listening1.append(u)

    sending2 = []
    listening2 = sending1

    for u in g.nodes:
        if u not in inactive:
            if u in listening1:
                heard = False
                for v in g.neighbors(u):
                    if v in sending1:
                        heard = not heard
                        if heard == False:
                            break
                if heard:
                    sending2.append(u)

    sending3 = []
    listening3 = sending2

    for u in g.nodes:
        if u not in inactive:
            if u in listening2:
                heard = False
                for v in g.neighbors(u):
                    if v in sending2:
                        heard = not heard
                        if heard == False:
                            break
                if heard:
                    inactive.add(u)
                    sending3.append(u)

    for u in g.nodes:
        if u not in inactive:
            if u in listening3:
                heard = False
                for v in g.neighbors(u):
                    if v in sending3:
                        heard = not heard
                        if heard == False:
                            break
                if heard:
                    inactive.add(u)

    rounds.extend([sending1, listening1, sending2, listening2, sending3, listening3])

round_info = map(lambda round: ' '.join(map(lambda x: str(x), round)) + '\n', rounds)

with open(out, 'w') as file:
    # Write to file in the following format:
    #
    #   Name
    #   Upper bound on n
    #   Upper bound on Delta
    #   Constant (C * log n log Delta)
    #   Number of nodes
    #   Number of edges
    #   Points (x y)
    #   Edges (u v)
    #   Round info (IDs of nodes that are active in that round)
    #
    # This is enough to reconstruct the simulation

    file.writelines([
        name + '\n',
        str(n_est) + '\n',
        str(d_est) + '\n',
        str(c) + '\n',
        str(n) + '\n',
        str(m) + '\n'
    ])
    file.writelines(map(lambda point: f'{point[0]} {point[1]}\n', points))
    file.writelines(edges)
    file.writelines(round_info)