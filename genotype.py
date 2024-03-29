import numpy as np
import random
import copy
from evaluation import Evaluation


class Genotype:
    def __init__(self, graph, n_edges):
        self.eval = Evaluation()
        self.graph = graph
        self.n_edges = n_edges
        self.yes_mutation = 0
        self.no_mutation = 0
        self.yes_recombination = 0
        self.no_recombination = 0
        
    def initialize(self, node_num):
        x = ''.join(random.choice('01') for _ in range(node_num))
        return x, self.eval.get_fitness(self.graph, x, self.n_edges)


    def one_bit_mutate(self, x):
        rand_idx = random.randint(0, len(x)-1) # 0 <= rand_idx <= len(x1)-1
        new_x = x[:rand_idx] + ('1' if x[rand_idx] == '0' else '0') + x[rand_idx+1:] 
        return new_x, self.eval.get_fitness(self.graph, new_x, self.n_edges)
    
    def targeted_one_bit_mutate(self, x, choose_num=10):
        ret_pool = []
        
        for _ in range(choose_num):
            i = random.randint(0, len(x)-1)
            fin = self.eval.fitness_increase(self.graph, x, i)
            # if fin > 0:
            new_x = x[:i] + ('1' if x[i] == '0' else '0') + x[i+1:]
            ret_pool.append((new_x, fin))
        np.random.shuffle(ret_pool)
        ret_pool.sort(key=lambda tup: tup[1], reverse=True)
        return ret_pool[0][0], self.eval.get_fitness(self.graph, ret_pool[0][0], self.n_edges)
    
    def bit_wise_mutate(self, x, alpha=0.01):
        for i in range(len(x)):
            if random.random() < alpha:
                x = x[:i] + ('1' if x[i] == '0' else '0') + x[i+1:]
        return x, self.eval.get_fitness(self.graph, x, self.n_edges)
    
    def one_point_xover(self, x1, x2):
        rand_idx = random.randint(0, len(x1)-2) # 0 <= rand_idx <= len(x1)-2
        new_x1 = x1[:rand_idx] + x2[rand_idx:]
        new_x2 = x2[:rand_idx] + x1[rand_idx:]
        return (new_x1, self.eval.get_fitness(self.graph, new_x1, self.n_edges)), (new_x2, self.eval.get_fitness(self.graph, new_x2, self.n_edges))