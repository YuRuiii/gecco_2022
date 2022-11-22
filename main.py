import networkx as nx
import numpy as np
import argparse
from graph import Graph
from genotype import Genotype
from evaluation import Evaluation
from population import Population


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph-type', type=str, help='graph type', default='regular')
    parser.add_argument('--n-nodes', type=int, help='the number of nodes', default=12)
    parser.add_argument('--n-d', type=int, help='the number of degrees for each node', default=10)
    parser.add_argument('--T', type=int, help='the number of fitness evaluations', default=10000)
    parser.add_argument('--seed-g', type=int, help='the seed of generating regular graph', default=1)
    parser.add_argument('--seed', type=int, default=2023)
    parser.add_argument('--gset-id', type=int, default=1)
    parser.add_argument('--sigma', type=float, help='hyper-parameter of mutation operator',default=.1)
    parser.add_argument('--population_size', type=int, default=10)
    args = parser.parse_known_args()[0]
    return args


def main(args=get_args()):
    print(args)
    g = Graph()
    # get graph
    graph, n_nodes, n_edges = g.graph_generator(args.graph_type, args.n_d, args.n_nodes, args.seed_g, args.gset_id)
    np.random.seed(args.seed)
    popu = Population(graph, n_nodes, n_edges, args.population_size)
    print("graph, node num =", n_nodes, "edge num =", n_edges)
    print("start training...")
    best_fitness = 0 
    with open('test.txt', 'w') as file:
        for i in range(1, args.T):
            _, tmp_fitness = popu.iterate()
            file.write('%s %s\n'%(str(i), str(tmp_fitness)))
            print(i, tmp_fitness)
            assert i <= 20
            # if tmp_fitness > best_fitness:
            #     best_fitness = tmp_fitness
            #     print(i, best_fitness)
            # print([f[-1] for f in popu.plist])
        
if __name__ == '__main__':
    main()
