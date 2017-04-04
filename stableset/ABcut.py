'''
Source: http://stackoverflow.com/questions/39472910/fast-way-to-get-edges-crossing-two-sets-of-nodes-in-networkx-graph
'''

import networkx


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