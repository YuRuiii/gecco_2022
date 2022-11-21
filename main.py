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
    parser.add_argument('--n-nodes', type=int, help='the number of nodes', default=10000)
    parser.add_argument('--n-d', type=int, help='the number of degrees for each node', default=10)
    parser.add_argument('--T', type=int, help='the number of fitness evaluations', default=10000)
    parser.add_argument('--seed-g', type=int, help='the seed of generating regular graph', default=1)
    parser.add_argument('--seed', type=int, default=2023)
    parser.add_argument('--gset-id', type=int, default=1)
    parser.add_argument('--sigma', type=float, help='hyper-parameter of mutation operator',default=.1)
    args = parser.parse_known_args()[0]
    return args


def main(args=get_args()):
    print(args)
    g = Graph()
    
    # get graph
    graph, n_nodes, n_edges = g.graph_generator(args.graph_type, args.n_d, args.n_nodes, args.seed_g, args.gset_id)
    np.random.seed(args.seed)
    popu = Population(graph, n_nodes, n_edges, 100)
    print(n_nodes, n_edges)
    
    for i in range(1, args.T):
        _, best_fitness = popu.iterate()
        print(i, best_fitness)  
        # print(i, best_fitness, [popu.population[i][1] for i in range(len(popu.population))])

if __name__ == '__main__':
    main()
