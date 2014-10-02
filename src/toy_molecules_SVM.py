import networkx as nx
from itertools import chain, combinations
from matplotlib import pyplot


# node designation to atom combination 
LABELS_mapping = {'a':'CH3', 'b':'OH', 'c':'C', 'd':'NH2', 'e':'Cl'}

mol1 = nx.Graph()
mol1.add_nodes_from(range(6))
mol1.add_edges_from([(0, 1, {'type' : 1}), (1, 2, {'type' : 1}), 
                     (1, 3, {'type' : 2}), (3, 4, {'type' : 1}), 
                     (5, 3, {'type' : 1})])

# for now before adding labels the molecules are all the same
# 1,2,3,4 are  positive examples, 5,6,7 are negative examples
# 8,9 are test examples
mol2, mol3, mol4 = mol1.copy(), mol1.copy(), mol1.copy()
pos_examples = set([mol1, mol2, mol3, mol4])
mol5, mol6, mol7 = mol1.copy(), mol1.copy(), mol1.copy()
neg_examples = set([mol5, mol6, mol7])
mol8, mol9 = mol1.copy(), mol1.copy()
mol10 = mol1.copy()
test_examples = set([mol8, mol9, mol10])


LABELS = {mol1 : ['a', 'c', 'b', 'c', 'd', 'd'],
          mol2 : ['a', 'c', 'b', 'c', 'd', 'b'],
          mol3 : ['a', 'c', 'b', 'c', 'e', 'a'],
          mol4 : ['a', 'c', 'e', 'c', 'b', 'e'],
          mol5 : ['a', 'c', 'd', 'c', 'd', 'd'],
          mol6 : ['d', 'c', 'b', 'c', 'a', 'e'],
          mol7 : ['d', 'c', 'b', 'c', 'd', 'e'],
          mol8 : ['a', 'c', 'b', 'c', 'e', 'd'],
          mol9 : ['d', 'c', 'a', 'c', 'b', 'e'],
          mol10 : ['a', 'c', 'b', 'c', 'd', 'd'] }

for mol in pos_examples.union(neg_examples).union(test_examples):
    for i in xrange(6):
        mol.node[i]['label'] = LABELS[mol][i]

# print mol1.adjacency_list()
# print mol1.edge[1][3]['type']
# print mol9.node[5]['label']
# print mol1.subgraph([0,1,2,3]).node[3]['label']

def powerset_iter(some_set):
    for subset in chain.from_iterable(combinations(some_set, r) 
                                      for r in range(len(some_set)+1)):
        yield set(subset)

# def powerset(some_set):
#     ar = []
#     for subset in chain.from_iterable(combinations(some_set, r) 
#                                       for r in range(len(some_set)+1)):
#         ar.append(set(subset))
#     return ar
                
# def subgraph_iter(graph, min_n_edges):
#     for i in powerset_iter(set(graph.edges())):
#         print i
#         if len(i) >= min_n_edges:
#             yield nx.Graph(tuple(i))

def subgraph_iter(graph, min_n_nodes):
    for i in powerset_iter(set(graph.nodes())):
        if len(i) >= min_n_nodes:
            subgraph = graph.subgraph(tuple(i))
            if nx.is_connected(subgraph):
                yield subgraph
            
# def all_subgraphs(graph):
#     ar = []
#     for i in powerset_iter(set(range(len(graph)))):
#         ar.append(graph.subgraph(i))
#     return ar

# def all_subgraphs_larger_n_edges(graph, n):
#     ar = []
#     for i in powerset_iter(graph.edges()):
#         if i.number_of_edges() >= n:
#             ar.append(nx.Graph(tuple(i)))
#     return ar

def node_match(n1,n2):
    return n1['label'] == n2['label']

def edge_match(e1,e2):
    return e1['type'] == e2['type']

def all_training_graphlets(training_set, min_n_edges):
    def unique_subgparh(example_subgraph, graphlets):
        for graphlet in graphlets:
#             if nx.is_isomorphic(example_subgraph, graphlet, 
#                                 node_match=node_match, 
#                                 edge_match = edge_match):
            if nx.is_isomorphic(example_subgraph, graphlet, 
                                node_match=node_match, 
                                edge_match = edge_match):
                return False
        return True
    
    graphlets = []
    for example in training_set:
        for example_subgraph in subgraph_iter(example, min_n_edges):
            if unique_subgparh(example_subgraph, graphlets):
                graphlets.append(example_subgraph)
    return graphlets

def draw_molecule(mol):
    col = {'a' : 1, 'b': 0.75, 'c': 0.55, 'd': 0.67, 'e':0}
    edge_labels=dict([((u,v,),d['type'])
                 for u,v,d in mol.edges(data=True)])
    colors = [col.get(mol.node[node]['label']) for node in mol.nodes()]
    pos = nx.spring_layout(mol)
    labels = {}
    for i in mol.nodes():
        labels[i] = LABELS_mapping.get(mol1.node[i]['label']) 

    nx.draw_networkx(mol, pos, node_size=3000, 
            node_color = colors, edge_labels=edge_labels,
            labels = labels)
    pyplot.show()

 
if __name__ == "__main__":    
    min_nodes = 6
    graphlets = all_training_graphlets(pos_examples.union(neg_examples), min_nodes)
    print str(len(graphlets)) + " " + str(min_nodes) + "-graphlets build." 
    # draw_molecule(mol1)
        
    for graphlet in graphlets:
        draw_molecule(graphlets)
    
    # print hash(tuple(mol1.nodes())), hash(tuple(mol6.nodes()))

  
