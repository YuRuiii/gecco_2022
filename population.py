from genotype import Genotype
from evaluation import Evaluation

class Population:
    def __init__(self, graph, n_nodes, n_edges, size):
        self.max_size = size
        self.plist = []
        self.geno = Genotype()
        self.eval = Evaluation()
        self.graph = graph
        self.n_edges = n_edges
        for _ in range(100):
            x = self.geno.initialize(n_nodes)
            self.plist.append((x, self.eval.get_fitness(graph, x, n_edges)))
        
    def iterate(self):
        new_plist = []
        for g in self.plist:
            tmp = self.geno.bit_wise_mutate(g[0])
            tmp_fitness = self.eval.get_fitness(self.graph, tmp, self.n_edges)
            new_plist.append((tmp, tmp_fitness))
        self.plist += new_plist
        self.update()
        best_fitness = self.plist[0][1]
        return self.plist[0], best_fitness
        
    def update(self):
        if(len(self.plist) > self.max_size):
            self.plist.sort(key=lambda tup: tup[1], reverse=True)
        self.plist = self.plist[:self.max_size]
        # print(self.population)
        
    