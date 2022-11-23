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
        # print(self.eval.get_fitness(self.graph, new_x, self.n_edges))
        # print(self.eval.get_fitness(self.graph, x, self.n_edges))
        if self.eval.get_fitness(self.graph, new_x, self.n_edges) > self.eval.get_fitness(self.graph, x, self.n_edges):
            self.yes_mutation += 1
            # print("yes from mutation")
        else:
            self.no_mutation += 1
            # print("no from mutation") 
        return new_x, self.eval.get_fitness(self.graph, new_x, self.n_edges)
    
    
    # def bit_wise_mutate(self, x, alpha):
    #     new_x = list(x)
    #     for i in range(0, len(x)-1):
    #         if random.random() < alpha:
    #             new_x[i] = 1 if x[i] == 0 else 0
    #     new_x = np.array(new_x).astype(int)
    #     return new_x
    
    
    def one_point_xover(self, x1, x2):
        rand_idx = random.randint(0, len(x1)-2) # 0 <= rand_idx <= len(x1)-2
        new_x1 = x1[:rand_idx] + x2[rand_idx:]
        new_x2 = x2[:rand_idx] + x1[rand_idx:]
        # print(self.eval.get_fitness(self.graph, new_x1, self.n_edges))
        # print(self.eval.get_fitness(self.graph, new_x2, self.n_edges))
        # print(self.eval.get_fitness(self.graph, x1, self.n_edges))
        # print(self.eval.get_fitness(self.graph, x2, self.n_edges))
        
        if self.eval.get_fitness(self.graph, new_x1, self.n_edges) > max(self.eval.get_fitness(self.graph, x1, self.n_edges), self.eval.get_fitness(self.graph, x2, self.n_edges)):
            self.yes_recombination += 1
            # print("yes from recombination")
        else:
            self.no_recombination += 1
            # print("no from recombination") 
        if self.eval.get_fitness(self.graph, new_x2, self.n_edges) > max(self.eval.get_fitness(self.graph, x1, self.n_edges), self.eval.get_fitness(self.graph, x2, self.n_edges)):
            self.yes_recombination += 1
            # print("yes from recombination")
        else:
            self.no_recombination += 1
            # print("no from recombination") 
        return (new_x1, self.eval.get_fitness(self.graph, new_x1, self.n_edges)), (new_x2, self.eval.get_fitness(self.graph, new_x2, self.n_edges))
    
    
    def mutate(self, x, alpha=0.01):
        return self.one_bit_mutate(x)
    
    
    def recombine(self, x1, x2):
        return self.one_point_xover(x1, x2)
    
    