from genotype import Genotype
from evaluation import Evaluation
import random
import numpy as np

class Population:
    def __init__(self, graph, n_nodes, n_edges, size):
        self.max_size = size
        self.max_mating_pool_size = size
        self.recombination_time = size / 2
        self.geno = Genotype()
        self.eval = Evaluation()
        self.graph = graph
        self.n_nodes = n_nodes
        self.n_edges = n_edges
        self.plist = []
        for _ in range(size):
            x = self.geno.initialize(self.n_nodes)
            self.plist.append(tuple(np.append(x, self.eval.get_fitness(self.graph, x, self.n_edges))))
        # print(self.plist)
        # assert 0
 
 
    # parent selection: fitness proportional selection, with windowing
    def FPS(self):
        # print("plist:", self.plist)
        min_fitness = min([x[-1] for x in self.plist])
        normalized_plist = [(x[:-1], x[-1] - min_fitness) for x in self.plist]
        sum_fitness = sum(f for _, f in normalized_plist)
        if sum_fitness == 0:
            print("sum_fitness == 0")
            # print(1 / len(normalized_plist))
            prob_plist = [(normalized_plist[i][0], 1 / len(normalized_plist)) for i in range(len(normalized_plist))]
        else:
            prob_plist = [(normalized_plist[i][0], normalized_plist[i][1] / sum_fitness) for i in range(len(normalized_plist))]
        return prob_plist
    
    
    # implementation of sampling
    def stochastic_universal_sampling(self, prob_plist):
        mating_pool = []
        r = random.uniform(0, 1 / self.max_mating_pool_size)
        a = 0
        for i in range(len(prob_plist)):
            a += prob_plist[i][1]
            while r <= a:
                # print(i, end="")
                mating_pool.append(prob_plist[i][0])
                r += 1 / self.max_mating_pool_size
        # print("")
        return mating_pool
    
    
    def get_prob_list(self):
        return self.FPS()
    
    def get_mating_pool(self, prob_plist):
        return self.stochastic_universal_sampling(prob_plist)
            
            
    def get_parent(self):
        return self.plist
        prob_plist = self.get_prob_list()
        # return [prob_plist[i][0] for i in range(len(prob_plist))]
        # print("prob_list:", prob_plist)
        mating_pool = self.get_mating_pool(prob_plist)
        # print("mating_pool:", mating_pool)
        # assert 0
        return mating_pool
    
    
    def get_offspring(self, mating_pool):
        np.random.shuffle(mating_pool)
        offspring = []
        
        # recombination
        # for i in range(len(mating_pool) // 2):
        #     child1, child2 = self.geno.recombine(mating_pool[2*i], mating_pool[2*i+1])
        #     for c in child1, child2:
        #         c = list(c)
        #         c.append(self.eval.get_fitness(self.graph, child2, self.n_edges))
        #         c = tuple(c)
        #         offspring.append(c)

        # mutation
        for node in mating_pool:
            c = self.geno.mutate(node)
            c = list(c)
            c[-1] = self.eval.get_fitness(self.graph, c[:-1], self.n_edges)
            # c.append(self.eval.get_fitness(self.graph, c, self.n_edges))
            # c = tuple(c)
            print(c, node, len(c), len(node))
            offspring.append(c)
        return offspring
    
        
    def iterate(self):
        parent = self.get_parent()
        offspring = self.get_offspring(parent)
        self.survivor_selection(offspring)
        
        for ele in self.plist:
            assert len(ele) == self.n_nodes + 1
        return self.plist, self.plist[-1][-1]
        
    def survivor_selection(self, offspring):
        # print(offspring)
        # assert 0
        # new_plist = np.unique(self.plist, axis=0)
        new_plist = np.append(self.plist, offspring, axis=0)
        # new_plist[:, :-1] = new_plist[:, :-1].astype(int)
        # new_plist[:, -1] = new_plist[:, -1].astype(float)
        # print(new_plist)
        # print([type(ele) for ele in new_plist[0]])
        new_plist = np.unique(new_plist, axis=0)
        # new_plist = [list(np.unique(x)) for x in new_plist]
        # new_plist = set([tuple(x) for x in new_plist])
        
        # print(new_plist)
        # assert 0
        # new_plist = self.plist + offspring
        # print(new_plist)
        new_plist = new_plist[new_plist[:, -1].argsort()]
        # new_plist = sorted(new_plist, axis=0)
        # print(new_plist)
        # assert 0
        # print([ele[-1] for ele in new_plist])
        # new_plist.sort(key=lambda x: x[-1], reverse=True)
        self.plist = new_plist[-self.max_size:]
        # print(self.plist)
        
    