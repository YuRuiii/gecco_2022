import numpy as np
import random
import copy


class Genotype:
    def initialize(self, node_num):
        return np.random.randint(2, size=node_num)
    
    def bit_wise_mutate(self, x):
        rand_idx = random.randint(0, x.size-1)
        new_x = copy.deepcopy(x)
        new_x[rand_idx] = 1 if new_x[rand_idx] == 0 else 0
        return new_x
    
    