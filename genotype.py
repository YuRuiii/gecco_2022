import numpy as np
import random
import copy


class Genotype:
    def initialize(self, node_num):
        return np.random.randint(2, size=node_num)
    
    def one_bit_mutate(self, x):
        rand_idx = random.randint(0, x.size-1)
        new_x = copy.deepcopy(x)
        new_x[rand_idx] = 1 if x[rand_idx] == 0 else 0
        return new_x
    
    def bit_wise_mutate(self, x, alpha):
        new_x = list(x)
        for i in range(0, len(x)-1):
            if random.random() < alpha:
                new_x[i] = 1 if x[i] == 0 else 0
        new_x = np.array(new_x).astype(int)
        return new_x
    
    def one_point_xover(self, x1, x2):
        rand_idx = random.randint(0, len(x1)-2) # 0 <= rand_idx <= len(x1)-2
        new_x1 = np.concatenate((list(x1[:rand_idx]), list(x2[rand_idx:])), axis=None).astype(int)
        new_x2 = np.concatenate((list(x2[:rand_idx]), list(x1[rand_idx:])), axis=None).astype(int)
        return new_x1, new_x2
    
    def mutate(self, x, alpha=0.01):
        return self.bit_wise_mutate(x, alpha)
    
    def recombine(self, x1, x2):
        return self.one_point_xover(x1, x2)
    