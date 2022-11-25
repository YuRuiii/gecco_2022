import numpy as np
import networkx as nx


class Evaluation:
    def get_fitness(self, graph, c, n_edges):
        node = np.array(list(c))
        g1 = np.where(node == '1')[0]
        g2 = np.where(node == '0')[0]
        return nx.cut_size(graph, g1, g2) / n_edges
    
    
    def fitness_increase(self, graph, x, idx):
        # 左多了idx,右少了idx
        # cut=node1在左边，node2在右边的边数
        # 改变之后，左边多了node1，cut_size - 原来和node1相连的左边结点 + 原来和node1相连的右边结点
        edges = graph.edges(idx)
        nodes = [tup[1] for tup in edges]
        same_cnt, diff_cnt = 0, 0
        for n in nodes:
            if x[n] == x[idx]:
                same_cnt += 1
            else:
                diff_cnt += 1
        return same_cnt - diff_cnt
        