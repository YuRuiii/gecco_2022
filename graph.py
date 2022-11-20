import networkx as nx

class Graph:
    def generate_regular_graph(self, n_d, n_nodes, seed_g):
        graph = nx.random_graphs.random_regular_graph(d=n_d, n=n_nodes, seed=seed_g)
        return graph, len(graph.nodes), len(graph.edges)
    
    def generate_gset_graph(self, gset_id):
        # 这里提供了比较流行的图集合: Gset, 用于进行分割
        dir = './Gset/'
        fname = dir + 'G' + str(gset_id) + '.txt'
        graph_file = open(fname)
        n_nodes, n_e = graph_file.readline().rstrip().split(' ')
        print(n_nodes, n_e)
        nodes = [i for i in range(int(n_nodes))]
        edges = []
        for line in graph_file:
            n1, n2, w = line.split(' ')
            edges.append((int(n1) - 1, int(n2) - 1, int(w)))
        graph = nx.Graph()
        graph.add_nodes_from(nodes)
        graph.add_weighted_edges_from(edges)
        return graph, len(graph.nodes), len(graph.edges)

    def graph_generator(self, graph_type, n_d, n_nodes, seed_g, gset_id):
        if graph_type == 'regular':
            return self.generate_regular_graph(n_d, n_nodes, seed_g)
        elif graph_type == 'gset':
            return self.generate_gset_graph(gset_id)
        else:
            raise NotImplementedError(f'Wrong graph_tpye')

