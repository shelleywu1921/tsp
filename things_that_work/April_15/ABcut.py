'''
Source: http://stackoverflow.com/questions/39472910/fast-way-to-get-edges-crossing-two-sets-of-nodes-in-networkx-graph

Warning: the edge returned is an ordered pair!!
'''




import networkx as nx

# edges_cross
def edges_cross(graph, nodes1, nodes2):
    """
        Finds edges between two sets of disjoint nodes.
        Running time is O(len(nodes1) * len(nodes2))
        
        Args:
        graph (nx.Graph): an undirected graph
        nodes1 (set): set of nodes disjoint from nodes2
        nodes2 (set): set of nodes disjoint from nodes1.
        """
	return {(u, v) for u in nodes1
		for v in nodes2.intersection(graph.adj[u])}


## Test
## passed
'''
def test_edge_cross():
    G = nx.Graph()
    G.add_nodes_from(range(10))
    G.add_edges_from([(0,6),(1,7),(2,8),(3,9)])
    G.add_edges_from([(2,5),(4,7)])
    G.add_edges_from([(0,2),(3,4),(5,9)])

    A=set([0])
    B=set([6])
    
    C=set([2,3])
    D=set([6,7])
    
    E=set(range(5))
    F=set(range(5,10))
    
    assert edges_cross(G, A,B) == set([(0,6)])
    assert len(edges_cross(G,C,D))==0
    assert edges_cross(G,E,F)==set([ (0,6),(1,7),(2,8),(3,9),(2,5),(4,7)])
'''