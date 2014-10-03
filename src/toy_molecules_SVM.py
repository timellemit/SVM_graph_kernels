import networkx as nx
from itertools import chain, combinations
from matplotlib import pyplot

# for simplicity we map atom combinations to letters
LABELS_mapping = {'a':'CH3', 'b':'OH', 'c':'C', 'd':'NH2', 'e':'Cl'}

def make_data(num_pos_examples, 
              num_neg_examples, num_test_examples, num_nodes):
    pos_label_matrix = [['a', 'c', 'b', 'c', 'd', 'd'], 
                        ['a', 'c', 'b', 'c', 'd', 'b'],
                        ['a', 'c', 'b', 'c', 'e', 'a'], 
                        ['a', 'c', 'e', 'c', 'b', 'e']]
    neg_label_matrix = [['a', 'c', 'd', 'c', 'd', 'd'], 
                        ['d', 'c', 'b', 'c', 'a', 'e'],
                        ['d', 'c', 'b', 'c', 'd', 'e']]
    test_label_matrix = [['a', 'c', 'b', 'c', 'e', 'd'],
                         ['d', 'c', 'a', 'c', 'b', 'e']] 
    
    template_molecule = nx.Graph()
    template_molecule.add_nodes_from(range(num_nodes))
    # the structure of a molecule is hardcoded
    template_molecule.add_edges_from([(0, 1, {'type' : 1}), 
        (1, 2, {'type' : 1}), (1, 3, {'type' : 2}), 
        (3, 4, {'type' : 1}), (5, 3, {'type' : 1})])
    pos_examples = [template_molecule.copy() 
                    for i in xrange(num_pos_examples)]  # @UnusedVariable
    neg_examples = [template_molecule.copy() 
                    for i in xrange(num_neg_examples)]  # @UnusedVariable
    test_examples = [template_molecule.copy() 
                     for i in xrange(num_test_examples)] # @UnusedVariable
    for (molecules, label_matrix) in zip((pos_examples, neg_examples, test_examples), 
                                         (pos_label_matrix, neg_label_matrix, test_label_matrix)):
        for i in xrange(len(molecules)):
            for j in xrange(num_nodes):
                molecules[i].node[j]['label'] = label_matrix[i][j]
   
    return pos_examples, neg_examples, test_examples

# draws a molecule (hardcoded)
def draw_molecule(mol):
    col = {'a' : 1, 'b': 0.75, 'c': 0.35, 'd': 0.67, 'e':0}
    colors = [col.get(mol.node[node]['label']) for node in mol.nodes()]
    pos = nx.spring_layout(mol)
    labels = {}
    for i in mol.nodes():
        labels[i] = LABELS_mapping.get(mol.node[i]['label']) 

    nx.draw_networkx(mol, pos, node_size=3000, 
            node_color = colors, labels = labels)
    pyplot.show()
            
def powerset_iter(some_set):
    for subset in chain.from_iterable(combinations(some_set, r) 
                                      for r in range(len(some_set)+1)):
        yield set(subset)

# iterator for all connected subgraphs of a given graph 
# with number of nodes >= min_n_nodes
def subgraph_iter(graph, min_n_nodes):
    for i in powerset_iter(set(graph.nodes())):
        if len(i) >= min_n_nodes:
            subgraph = graph.subgraph(tuple(i))
            if nx.is_connected(subgraph):
                yield subgraph
            
# def all_training_graphlets(training_set, min_n_edges):
#     def node_match(n1,n2):
#         return n1['label'] == n2['label']
#     def edge_match(e1,e2):
#         return e1['type'] == e2['type']
#     def unique_subgraph(example_subgraph, graphlets):
#         for graphlet in graphlets:
# #             if nx.is_isomorphic(example_subgraph, graphlet)
#             if nx.is_isomorphic(example_subgraph, graphlet, 
#                                 node_match=node_match, 
#                                 edge_match = edge_match):
#                 return False
#         return True
#      
#     graphlets = []
#     for example in training_set:
#         for example_subgraph in subgraph_iter(example, min_n_edges):
#             if unique_subgraph(example_subgraph, graphlets):
#                 graphlets.append(example_subgraph)
#     return graphlets

def graphlet_descriptions(desc_set, training_set, min_n_edges):
    def node_match(n1,n2):
        return n1['label'] == n2['label']
    def edge_match(e1,e2):
        return e1['type'] == e2['type']
    def unique_subgraph(example_subgraph, graphlets):
        for graphlet in graphlets:
#             if nx.is_isomorphic(example_subgraph, graphlet)
            if nx.is_isomorphic(example_subgraph, graphlet, 
                                node_match=node_match, 
                                edge_match = edge_match):
                return False
        return True
    
    graphlets = []
    for example_ind in xrange(len(training_set)):
        new_graphlets = []
        for example_subgraph in subgraph_iter(training_set[example_ind], min_n_edges):
            if unique_subgraph(example_subgraph, graphlets):
                new_graphlets.append(example_subgraph)
        graphlets.extend(new_graphlets)
                
    desc_vectors = []
    for example_ind in xrange(len(desc_set)): 
        new_desc = []
        for example_subgraph in subgraph_iter(training_set[example_ind], min_n_edges):
            for graphlet_ind in xrange(len(graphlets)):
#                 draw_molecule(example_subgraph)
#                 draw_molecule(graphlets[graphlet_ind])
#                 print nx.is_isomorphic(example_subgraph, graphlets[graphlet_ind], 
#                                     node_match=node_match, edge_match = edge_match)
#                 print example_subgraph.node, graphlets[graphlet_ind].node, nx.is_isomorphic(example_subgraph, graphlets[graphlet_ind], 
#                                     node_match=node_match, edge_match = edge_match)
#                 desc_vectors[example_ind][graphlet_ind] = \
#                 1 if nx.is_isomorphic(example_subgraph, graphlets[graphlet_ind], 
#                                     node_match=node_match, edge_match = edge_match) \
#                 else 0
                new_desc.append(1 if nx.is_isomorphic(example_subgraph, graphlets[graphlet_ind], 
                                    node_match=node_match, edge_match = edge_match) else 0)
#                     desc_vectors[example_ind][graphlet_ind] = 1
        desc_vectors.append(new_desc)
                    
    return graphlets, desc_vectors

if __name__ == "__main__":  
    pos_examples, neg_examples, test_examples = make_data(num_pos_examples = 4, 
        num_neg_examples = 3, num_test_examples = 2, num_nodes = 6)
    min_nodes = 5
    graphlets, desc_vectors = graphlet_descriptions(pos_examples + neg_examples,
        pos_examples + neg_examples, min_nodes)
    def node_match(n1,n2):
        return n1['label'] == n2['label']
    def edge_match(e1,e2):
        return e1['type'] == e2['type']
    
    print nx.is_isomorphic(pos_examples[0], pos_examples[1])
    print nx.is_isomorphic(pos_examples[0], pos_examples[1], 
                                    node_match=node_match, edge_match = edge_match) 
    print len(graphlets), desc_vectors
    print str(len(graphlets)) + " " + str(min_nodes) + "-graphlets build." 
#     for graphlet in graphlets:
#         draw_molecule(graphlet)