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


# build_support_graph
'''
build_support_graph(fracsolu) takes a fractional solution to the TSP (a .x file) and returns F, the support graph of the fractional solution

Requirements:
    fracsolu is a .x file
    
Examples:
    build_support_graph('pr76.x')
'''

def build_support_graph(fracsolu):
    start=timer()
    
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
    end=timer()
    print('Running time: %.5f seconds' %(end-start))
    return F


## Testing build_support_graph
## passed
'''
if __name__ =="__main__":
    F=build_support_graph('pr76.x')
    #    print('Number of edges: %d' % F.number_of_edges())
    #    print('Number of nodes: %d' % F.number_of_nodes()) # this prints the edge weights as well
    print(list(F.edges(data=True)))
'''

## one more test for pr76
## passed
'''
def test_build_support_graph_pr76():
    F=build_support_graph('pr76.x')
    assert F.number_of_edges()==95
    assert F.number_of_nodes()==76
    assert F.has_edge(0,75)
    assert F.has_edge(0,22)
    assert F.has_edge(59,58)
    assert F.has_edge(74,75)
    assert not F.has_edge(1,75)
    assert not F.has_edge(0,0)
    assert F[0][75]['weight']==1.00000
'''

## test for att532
## passed
'''
if __name__ =="__main__":
    F=build_support_graph('att532.x')
    print('Number of edges: %d' % F.number_of_edges())
    print('Number of nodes: %d' % F.number_of_nodes())
    print(list(F.edges(data=True)))
'''

## one more test for pr76
## passed
'''
def test_build_support_graph_pr76():
    F=build_support_graph('att532.x')
    assert F.number_of_edges()==818
    assert F.number_of_nodes()==532
    assert F.has_edge(0,2)
    assert F.has_edge(0,1)
    assert F.has_edge(159,142)
    assert F.has_edge(496,486)
    assert not F.has_edge(1,75)
    assert not F.has_edge(0,0)
    assert F[21][27]['weight']==0.790773
'''





# add_s_t
'''
   
Requirement: 
    * candidate_dom: a list of nodes in G, such that the corresponding dominoes are disjoint
    * pattern: a string of {0,1} that has the same length as candidate_dom
               if pattern[i]==0, then the domino represented by candidate_dom[i] has A in handle and B bot in handle
'''

def add_s_t(F,G,candidate_dom, pattern):
    # determines what is in handle and what is not in handle according to the pattern
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
                
    # construct Fbar by adding s and t. s: inHandle, t: notinHandle
    Fbar=F
    



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
        