from genotype import Genotype
from evaluation import Evaluation
import random
import numpy as np

class Population:
    def __init__(self, graph, n_nodes, n_edges, size):
        self.max_size = size
        self.max_mating_pool_size = size
        self.recombination_time = size / 2
        self.geno = Genotype(graph, n_edges)
        self.eval = Evaluation()
        self.graph = graph
        self.n_nodes = n_nodes
        self.n_edges = n_edges
        self.plist = []
        for _ in range(size):
            node_info = self.geno.initialize(n_nodes)
            self.plist.append(node_info)
 
    # parent selection: fitness proportional selection, with windowing
    def FPS(self):
        # print("plist:", self.plist)
        min_fitness = min(x[1] for x in self.plist)
        normalized_plist = [(x, x[1] - min_fitness) for x in self.plist]
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
        for i in range(len(mating_pool) // 2):
            child1, child2 = self.geno.recombine(mating_pool[2*i][0], mating_pool[2*i+1][0])
            offspring.append(child1)
            offspring.append(child2)

        # mutation
        for parent, _ in mating_pool:
            off_info = self.geno.mutate(parent)
            offspring.append(off_info)
        return offspring
    
        
    def iterate(self):
        parent = self.get_parent()
        # print("parent:" , parent)
        offspring = self.get_offspring(parent)
        # print("offspring:", offspring)
        self.survivor_selection(offspring)
        return self.plist[0][0], self.plist[0][1]
        
    def survivor_selection(self, offspring):
        new_plist = list(set(self.plist + offspring)) # remove duplicates
        new_plist.sort(key=lambda tup: tup[1], reverse=True)
        self.plist = new_plist[:self.max_size]
        # print(self.plist)
        
    