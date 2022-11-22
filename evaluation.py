import numpy as np
import networkx as nx


class Evaluation:
    def get_fitness(self, graph, c, n_edges):
        node = np.array(list(c))
        g1 = np.where(node == '1')[0]
        g2 = np.where(node == '0')[0]
        # print(c, node, g1, g2, nx.cut_size(graph, g1, g2), n_edges)
        return nx.cut_size(graph, g1, g2) / n_edges