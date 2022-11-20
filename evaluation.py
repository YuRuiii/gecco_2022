import numpy as np
import networkx as nx


class Evaluation:
    def get_fitness(self, graph, x, n_edges):
        g1 = np.where(x == 1)[0]
        g2 = np.where(x == 0)[0]
        return nx.cut_size(graph, g1, g2) / n_edges