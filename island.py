import multiprocessing as mp
from multiprocessing import Pool, cpu_count
from population import Population
import random
import numpy as np

class Island:
    def __init__(self, graph, n_nodes, n_edges, population_size, stage, ex_ratio, ex_num, island_num=mp.cpu_count()):
        self.subpopu = []
        self.ex_ratio = ex_ratio
        self.ex_num = ex_num
        self.island_num = island_num
        self.iter_time = 0
        for _ in range(island_num):
            popu = Population(graph, n_nodes, n_edges, population_size, stage)
            self.subpopu.append(popu)
            
    def sub_iterate(self, idx):
        res = []
        for i in range(self.ex_ratio):
            tmp_fitness = self.subpopu[idx].iterate(i)[1]
            res.append(tmp_fitness)
            print(idx, i + self.iter_time * self.ex_ratio, tmp_fitness)
        return res
    
    def sub_exchange(self, i, j):
        # print("sub_exchange_1:", len(self.subpopu[i].plist))
        np.random.shuffle(self.subpopu[i].plist)
        np.random.shuffle(self.subpopu[j].plist)
        # print("before:")
        # print([tup[1] for tup in sorted(self.subpopu[i].plist, key=lambda tup: tup[1], reverse=True)])
        # print([tup[1] for tup in sorted(self.subpopu[j].plist, key=lambda tup: tup[1], reverse=True)])
        tmp1 = self.subpopu[i].plist[:self.ex_num]
        tmp2 = self.subpopu[j].plist[:self.ex_num]
        self.subpopu[i].plist = self.subpopu[i].plist[self.ex_num:] + tmp2
        self.subpopu[j].plist = self.subpopu[j].plist[self.ex_num:] + tmp1
        # print("sub_exchange_2:", len(self.subpopu[i].plist))
        # print("after:")
        # print([tup[1] for tup in sorted(self.subpopu[i].plist, key=lambda tup: tup[1], reverse=True)])
        # print([tup[1] for tup in sorted(self.subpopu[j].plist, key=lambda tup: tup[1], reverse=True)])
    
    def exchange(self):
        
        for i in range(self.island_num):
            j = random.randint(0, self.island_num-1)
            self.sub_exchange(i, j)
    
    def iterate(self, iter_time):
        self.iter_time = iter_time
        with mp.Pool(self.island_num) as pool:
            res = pool.map(self.sub_iterate, range(self.island_num))
            # print(res)
        flist = [max(res[j][i] for j in range(len(res))) for i in range(len(res[0]))]
        self.exchange()
        return flist
        