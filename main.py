import networkx as nx
import numpy as np
import argparse
from graph import Graph
from genotype import Genotype
from evaluation import Evaluation
from population import Population
from island import Island


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph-type', type=str, help='graph type', default='gset')
    parser.add_argument('--n-nodes', type=int, help='the number of nodes', default=1000)
    parser.add_argument('--n-d', type=int, help='the number of degrees for each node', default=10)
    parser.add_argument('--T', type=int, help='the number of fitness evaluations', default=1000)
    parser.add_argument('--seed-g', type=int, help='the seed of generating regular graph', default=1)
    parser.add_argument('--seed', type=int, default=2023)
    parser.add_argument('--gset-id', type=int, default=1)
    parser.add_argument('--sigma', type=float, help='hyper-parameter of mutation operator',default=.1)
    parser.add_argument('--population_size', type=int, default=10)
    parser.add_argument('--file', type=str, default='test.txt')
    parser.add_argument('--stage', type=int, default=1)
    
    args = parser.parse_known_args()[0]
    return args


def main(args=get_args()):
    print(args)
    g = Graph()
    # get graph
    graph, n_nodes, n_edges = g.graph_generator(args.graph_type, args.n_d, args.n_nodes, args.seed_g, args.gset_id)
    np.random.seed(args.seed)
    print("graph, node num =", n_nodes, "edge num =", n_edges)
    print("start training...")
    
    if args.stage == 1:
        popu = Population(graph, n_nodes, n_edges, args.population_size, args.stage)
        with open('fitness/'+args.file, 'w') as file1, open('info/'+args.file, 'w') as file2:
            for i in range(1, args.T):
                _, tmp_fitness = popu.iterate(i)
                file1.write('%s %s\n'%(str(i), str(tmp_fitness)))
                print(i, tmp_fitness)
                if i == 100: # save population
                    file2.write('%s '%(str(i)))
                    for ele in popu.plist:
                        file2.write('%s '%(str(ele)))
                    file2.write('\n')
    else:
        ex_ratio, ex_num = 50, 5
        island = Island(graph, n_nodes, n_edges, args.population_size, args.stage, ex_ratio, ex_num, 12)
        for i in range(0, args.T // ex_ratio + (0 if args.T % ex_ratio == 0 else 1)):
            flist = island.iterate(i)
            for idx, line in enumerate(flist):
                with open('fitness/'+args.file, 'a') as file:
                    file.write('%s %s\n'%(str(idx+i*ex_ratio), str(line)))
    
if __name__ == '__main__':
    main()
