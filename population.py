from genotype import Genotype
from evaluation import Evaluation
import random
import numpy as np

class Population:
    def __init__(self, graph, n_nodes, n_edges, size):
        self.max_size = size
        self.max_mating_pool_size = size
        self.recombination_time = size / 2
        self.plist = []
        self.geno = Genotype()
        self.eval = Evaluation()
        self.graph = graph
        self.n_edges = n_edges
        for _ in range(100):
            x = self.geno.initialize(n_nodes)
            self.plist.append((x, self.eval.get_fitness(graph, x, n_edges)))
 
 
    # parent selection: fitness proportional selection, with windowing
    def FPS(self):
        min_fitness = min(self.plist, key = lambda t: t[1])
        normalized_plist = [(self.plist[i][0], self.plist[i][1]-min_fitness) for i in range(len(self.plist))]
        sum_fitness = sum(normalized_plist, key = lambda t: t[1])
        prob_plist = [(self.plist[i][0], normalized_plist[i][1] / sum_fitness) for i in range(len(self.plist))]
        return prob_plist
    
    
    # implementation of sampling
    def stochastic_universal_sampling(self, prob_plist):
        mating_pool = []
        i = 0
        r = random.uniform(0, 1 / self.max_mating_pool_size)
        while len(mating_pool) <= self.max_mating_pool_size:
            while r <= prob_plist[i][1]:
                mating_pool.append(prob_plist[i][0])
                r += 1 / self.max_mating_pool_size
            i += 1
        return mating_pool
    
    
    def get_prob_list(self):
        return self.FPS()
    
    
    def get_mating_pool(self, prob_plist):
        return self.stochastic_universal_sampling(prob_plist)
            
            
    def get_parent(self):
        prob_plist = self.get_prob_list()
        mating_pool = self.get_mating_pool(prob_plist)
        return mating_pool
    
    
    def get_offspring(self, mating_pool):
        np.random.shuffle(mating_pool)
        offspring = []
        
        # recombination
        for i in range(len(mating_pool) // 2):
            child1, child2 = self.geno.recombine(mating_pool[2*i], mating_pool[2*i+1])
            offspring.append(child1)
            offspring.append(child2)
            
        # mutation
        for node in mating_pool:
            child = self.geno.mutate(node)
            offspring.append(child)
        
        off_plist = [(offspring[i], self.eval.get_fitness(self.graph, offspring[i], self.n_edges))]
        return off_plist
    
        
    def iterate(self):
        parent = self.get_parent()
        offspring = self.get_offspring(parent)
        self.plist += offspring
        self.survivor_selection()
        return self.plist[0][0], self.plist[0][1]
        
    def update(self):
        self.plist.sort(key=lambda tup: tup[1], reverse=True)
        self.plist = self.plist[:self.max_size]
        
    