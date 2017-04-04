import networkx as nx
from domgraph import find_stable_set
from itertools import product
from timeit import default_timer as timer


'''
A bit of notations: 
G denotes the graph where nodes represent dominoes
F denotes the support graph of x*
'''

'''
mindomcut2 is based on a different approach than mindomcut to find handles. Suppose we have an odd collection of
disjoint dominoes, where the A's are in H and the B's are not in H. 

Step1: Construct Fbar, a supergraph of F, as follows: add a vertex s to F, and edges (s,u) with huge edge weights (say 10) for all u in UnionA. Add another vertex t and edges (t,v) with huge edge weights for all v in UnionB.
Step2: Compute a min cost st cut in Fbar. If it represents an eligible handle, then the weight of the cut must <1 ==> the part containing s must also contain UnionA, and the part containing t must also contain UnionB
'''


'''
build_support_graph
'''

def build_support_graph(fracsolu):
    fracfile=open(fracsolu,'r')
    first_line=map(int,fracfile.readline().split())
    num_of_vertices=first_line[0]
    num_of_edges=first_line[1]
    
    F=nx.Graph()
    for i in range(num_of_edges):
        line=fracfile.readline().split()
        u=int(line[0])
        v=int(line[1])
        edge_wt=float(line[2])
        F.add_nodes_from([u,v])
        F.add_edge(u,v,weight=edge_wt)
    
    return F

def shrink_dom_graph(F,G,candidate_dom,pattern):
    inHandle=set()
    notinHandle=set()
    for i in range(len(candidate_dom)):
        domnode=candidate_dom[i]
        A=G.node[domnode]['A']
        B=G.node[domnode]['B']
        
        if pattern[i]==0:
            inHandle= inHandle.union(A)
            notinHandle=notinHandle.union(B)
        else:
            inHandle= inHandle.union(B)
            notinHandle=notinHandle.union(A)            
    Fshrink=F
    s=inHandle.pop()
    t=notinHandle.pop()
    
    for vertex in inHandle:
        Fshrink=nx.contracted_nodes(Fshrink,s,vertex, self_loops=False)
    for vertex in notinHandle:
        Fshrink=nx.contracted_nodes(Fshrink,t,vertex, self_loops=False)
    
    return [Fshrink,s,t, inHandle, notinHandle]

def find_handle(F,G,candidate_dom, total_surplus,vio_upper_bd):
    start=timer()
    all_patterns=list(product([0,1], repeat=len(candidate_dom)))
    for pattern in all_patterns:
        shrink=shrink_dom_graph(F,G,candidate_dom,pattern)
        Fshrink= shrink[0]
        s=shrink[1]
        t=shrink[2]
        inHandle=shrink[3]
        notinHandle=shrink[4]
        
        cutweight, partitions = nx.minimum_cut(Fshrink, s,t, capacity='weight')
        if cutweight + total_surplus < vio_upper_bd:
            edge_cut_list=[]
            for p1_node in partitions[0]:
                for p2_node in partitions[1]:
                    if Fshrink.has_edge(p1_node,p2_node):
                        edge_cut_list.append((p1_node,p2_node))
            end=timer()
            print('cut weight = %.5f' % cutweight)
            print('total surplus = %.5f' % total_surplus)
            print('cut weight + total surplus = %.5f' % cutweight+total_surplus)
            
            print('running time = %.5f seconds \n'% (end-start))
            
            return [cutweight, cutweight+total_surplus, edge_cut_list] 
            
def find_many_combs(F,G,vio_upper_bd, surplus_bound, ncombs):
    for i in range(ncombs):
        stable=find_stable_set(G,surplus_bound) 
        candidate_dom=stable[0]
        total_surplus=stable[1]
        find_handle(F,G,candidate_dom, total_surplus,vio_upper_bd)
        