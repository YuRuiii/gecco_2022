import numpy as np
import random
import copy


class Node:
    def initialization(self, node_num):
        return np.random.randint(2, size=node_num)
    
    def bit_wise_mutation(self, x):
        rand_idx = random.randint(0, x.size)
        new_x = copy.deepcopy(x)
        new_x[rand_idx] = 1 if new_x[rand_idx] == 0 else 0
        return new_x
    
    def graph_generator(self, args):
        if args.graph_type == 'regular':
            return self.generate_regular_graph(args)
        elif args.graph_type == 'gset':
            return self.generate_gset_graph(args)
        else:
            raise NotImplementedError(f'Wrong graph_tpye')