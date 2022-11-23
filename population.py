from genotype import Genotype
from evaluation import Evaluation
import random
import numpy as np
from tqdm import tqdm

class Population:
    def __init__(self, graph, n_nodes, n_edges, size, stage, init_expand=1):
        self.max_size = size
        self.max_mating_pool_size = size
        self.recombination_time = size / 2
        self.geno = Genotype(graph, n_edges)
        self.eval = Evaluation()
        self.graph = graph
        self.n_nodes = n_nodes
        self.n_edges = n_edges
        self.off_num = 1
        self.plist = []
        self.stage = stage
        if self.stage == 1:
            for _ in range(self.max_size):
                node_info = self.geno.initialize(n_nodes)
                self.plist.append(node_info)
        else:
            print("initializing...")
            init_pool = []
            for _ in tqdm(range(size * init_expand)):
                node_info = self.geno.initialize(n_nodes)
                init_pool.append(node_info)
            init_pool.sort(key=lambda tup: tup[1], reverse=True)
            self.plist = init_pool[:self.max_size]
                
 
    # parent selection: fitness proportional selection, with windowing
    def FPS(self):
        min_fitness = min(x[1] for x in self.plist)
        normalized_plist = [(x, x[1] - min_fitness) for x in self.plist]
        sum_fitness = sum(f for _, f in normalized_plist)
        if sum_fitness == 0:
            print("sum_fitness == 0")
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
                mating_pool.append(prob_plist[i][0])
                r += 1 / self.max_mating_pool_size
        return mating_pool
    
    
    def get_prob_list(self):
        return self.FPS()
    
    def get_mating_pool(self, prob_plist):
        return self.stochastic_universal_sampling(prob_plist)
            
            
    def get_parent(self):
        prob_plist = self.get_prob_list()
        mating_pool = self.get_mating_pool(prob_plist)
        return mating_pool
    
    
    def get_offspring(self, mating_pool=[]):
        offspring = []
        if self.stage == 1:
            np.random.shuffle(mating_pool)
            # recombination
            for i in range(len(mating_pool) // 2):
                child1, child2 = self.geno.one_point_xover(mating_pool[2*i][0], mating_pool[2*i+1][0])
                offspring.append(child1)
                offspring.append(child2)
            # mutation
            for parent, _ in mating_pool:
                off_info = self.geno.one_bit_mutate(parent)
                offspring.append(off_info)
            return offspring
        elif self.stage == 2:
            for parent, _ in self.plist:
                off_infos = self.geno.targeted_one_bit_mutate(parent, self.off_num)
                # print(_, off_infos[0][1])
                # assert(0)
                offspring += off_infos
                # off_info = self.geno.one_bit_mutate(parent)
                # offspring.append(off_info)
            print([i for _, i in offspring])
            return offspring
        else:
            assert 0
    
        
    def iterate(self, iter_time):
        if self.stage == 1:
            parent = self.get_parent()
            offspring = self.get_offspring(parent)
            self.survivor_selection(offspring)
        elif self.stage == 2:
            offspring = self.get_offspring()
            self.survivor_selection(offspring)
        else:
            assert 0
            
        return self.plist[0][0], self.plist[0][1]
        
    def survivor_selection(self, offspring):
        if self.stage == 1:
            new_plist = list(set(self.plist + offspring)) # remove duplicates
            new_plist.sort(key=lambda tup: tup[1], reverse=True)
            self.plist = new_plist[:self.max_size]
        elif self.stage == 2:
            self.plist = offspring
        else:
            assert 0
        
    