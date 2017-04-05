import networkx as nx
from domgraph import find_stable_set
from itertools import product
from timeit import default_timer as timer
from copy import copy

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
add_s_t(F,G,candidate_dom, pattern) takes F, the support graph of x*, G, a graph representing dominoes, candidate_dom, a list of disjoint dominoes with total weight <1, and pattern that says which half of a domino goes inside the handle. It returns [Fbar, inHandle, notinHandle]. 

Fbar is a supergraph of F with two extra vertices: 's' and 't'. (x,'s') is an edge if and only if x is in inHandle. Similarly, (y,'t') is an edge if and only if y is in notinHandle. All edges incident to 's' and 't' have weight 10

Example:
    from domgraph import create_dom_graph

    F=build_support_graph('pr76.x')
    G=create_dom_graph('pr76.dom', 0.5, 5000)
    candidate_dom,total_surplus = find_stable_set(G, total_surplus_bound)
    pattern='01001' # suppose candidate_dom has length 5

    add_s_t(F,G,candidate_dom, pattern)
    

Requirements:
    * candidate_dom: a list of nodes in G, such that the corresponding dominoes are disjoint. Total weight should <1
    * pattern: a string of {0,1} that has the same length as candidate_dom
               if pattern[i]=='0', then the domino represented by candidate_dom[i] has A in handle and B bot in handle
Warning:
    * Fbar and F are NOT aliases.
'''

def add_s_t(F,G,candidate_dom, pattern):
    # determines what is in handle and what is not in handle according to the pattern
    inHandle=set()
    notinHandle=set()
    for i in range(len(candidate_dom)):
        domnode=candidate_dom[i]
        A=G.node[domnode]['A']
        B=G.node[domnode]['B']

        if pattern[i]=='0':
            inHandle= inHandle.union(A)
            notinHandle=notinHandle.union(B)
        else:
            inHandle= inHandle.union(B)
            notinHandle=notinHandle.union(A)
                
    # construct Fbar by adding s and t. s: inHandle, t: notinHandle
    Fbar=copy(F)      # this is NOT an alias!
    Fbar.add_edges_from(list(('s',x) for x in inHandle), weight=100)
    Fbar.add_edges_from(list(('t',y) for y in notinHandle), weight=100)

    return [Fbar, inHandle, notinHandle]

## Testing time!
## for pr76
## check if inHandle and notinHandle match the pattern
## all passed
'''
def test_add_s_t_pr76_0():
    from domgraph import create_dom_graph
    F=build_support_graph('pr76.x')
    G=create_dom_graph('pr76.dom', 0.5, 5000)
    total_surplus_bound=0.75
    candidate_dom,total_surplus = find_stable_set(G, total_surplus_bound)
    pattern0='0'*len(candidate_dom)

    inH_0=set()
    ninH_0=set()
    
    for node in candidate_dom:
        A=G.node[node]['A']
        inH_0=inH_0.union(A)
        B=G.node[node]['B']
        ninH_0=ninH_0.union(B)

    Fbar, inHandle, notinHandle = add_s_t(F,G,candidate_dom,pattern0)
    assert inHandle==inH_0
    assert notinHandle==ninH_0


def test_add_s_t_pr76_1():
    from domgraph import create_dom_graph
    F=build_support_graph('pr76.x')
    G=create_dom_graph('pr76.dom', 0.5, 5000)
    total_surplus_bound=0.75
    candidate_dom,total_surplus = find_stable_set(G, total_surplus_bound)
    pattern1='1'*len(candidate_dom)

    inH_1=set()
    ninH_1=set()

    for node in candidate_dom:
        A=G.node[node]['A']
        B=G.node[node]['B']
        inH_1=inH_1.union(B)
        ninH_1=ninH_1.union(A)
    
    Fbar, inHandle, notinHandle = add_s_t(F,G,candidate_dom,pattern1)
    assert inHandle==inH_1
    assert notinHandle==ninH_1


def test_add_s_t_pr76_2():
    from domgraph import create_dom_graph
    F=build_support_graph('pr76.x')
    G=create_dom_graph('pr76.dom', 0.5, 5000)
    total_surplus_bound=0.75
    candidate_dom,total_surplus = find_stable_set(G, total_surplus_bound)
    pattern2='01'*len(candidate_dom)

    inH_2=set()
    ninH_2=set()
    
    for i in range(len(candidate_dom)):
        node = candidate_dom[i]
        A=G.node[node]['A']
        B=G.node[node]['B']
        if i%2==0:
            inH_2=inH_2.union(A)
            ninH_2=ninH_2.union(B)
        else:
            inH_2=inH_2.union(B)
            ninH_2=ninH_2.union(A)

    Fbar, inHandle, notinHandle = add_s_t(F,G,candidate_dom,pattern2)
    assert inHandle==inH_2
    assert notinHandle==ninH_2


def test_add_s_t_pr76_3():
    from domgraph import create_dom_graph
    F=build_support_graph('pr76.x')
    G=create_dom_graph('pr76.dom', 0.5, 5000)
    total_surplus_bound=0.75
    candidate_dom,total_surplus = find_stable_set(G, total_surplus_bound)
    pattern3='100'*len(candidate_dom)

    inH_3=set()
    ninH_3=set()

    for i in range(len(candidate_dom)):
        node = candidate_dom[i]
        A=G.node[node]['A']
        B=G.node[node]['B']
        if i%3==0:
            inH_3=inH_3.union(B)
            ninH_3=ninH_3.union(A)
        else:
            inH_3=inH_3.union(A)
            ninH_3=ninH_3.union(B)

    Fbar, inHandle, notinHandle = add_s_t(F,G,candidate_dom,pattern3)
    assert inHandle==inH_3
    assert notinHandle==ninH_3
'''

## test if Fbar has the correct number of nodes, if 's' is only adj to things in inHandle (similarly, 't'), and the weights of the new edges (s,x), (t,y) are correct (equals 10)
## passed
'''
def test_add_s_t_pr76_4():
    from domgraph import create_dom_graph
    import copy
    import networkx as nx
    F=build_support_graph('pr76.x')
    Fprime=copy.deepcopy(F)
    
    G=create_dom_graph('pr76.dom', 0.5, 5000)
    total_surplus_bound=0.75
    candidate_dom,total_surplus = find_stable_set(G, total_surplus_bound)
    pattern0='0'*len(candidate_dom)

    Fbar, inHandle, notinHandle = add_s_t(F,G,candidate_dom,pattern0)
    assert Fbar.number_of_nodes()==Fprime.number_of_nodes()+2
    assert Fbar.has_node('s')
    assert Fbar.has_node('t')
    assert Fbar.degree('s')==len(inHandle)
    assert Fbar.degree('t')==len(notinHandle)
    for neig in Fbar.neighbors('s'):
        assert Fbar['s'][neig]['weight'] ==10
        assert neig in inHandle
    for neig in Fbar.neighbors('t'):
        assert Fbar['t'][neig]['weight'] ==10
        assert neig in notinHandle

    from networkx import is_isomorphic
    Fbar.remove_node('s')
    Fbar.remove_node('t')
    assert is_isomorphic(Fbar,Fprime)
'''



# find_handle
'''
find_handle(F,G,candidate_dom, total_surplus, comb_upper_bd) takes
    F: the support graph of x*, 
    G: the graph representing dominoes, 
    candidate_dom: a list of nodes in G representing disjoint dominoes, 
    total_surplus: the total surplus of dominoes in candidate_dom
    comb_upper_bound: a float >=0, <1
and returns
    H: the handle found, if there is one with comb_surplus < comb_upper_bd
    None: if it couldnt find any handle as above


Example:
    from domgraph import create_dom_graph

    F=build_support_graph('pr76.x')
    G=create_dom_graph('pr76.dom', 0.5, 5000)
    candidate_dom,total_surplus = find_stable_set(G, total_surplus_bound)

    find_handle(F,G,candidate_dom,total_surplus, 0.9)
'''

def find_handle(F,G,candidate_dom, total_surplus,comb_upper_bd):
    start=timer()
    
    # for each node in candidate_dom, LHS =1/2surplus(Ti)-x*(E(A,B))
    # sumLHS = \sum 1/2 surplus(Ti)-x*(E(Ai,Bi)). Independ on H, the handle chosen
    LHS_list=[]
    for node in candidate_dom:
        A=G.node[node]['A']
        B=G.node[node]['B']
        
        from ABcut import edges_cross
        E_A_B=edges_cross(F,A,B)
        xE_A_B=sum(F[u][v]['weight'] for (u,v) in E_A_B)
        #        print('x*(E(A,B))=%.5f' % xE_A_B)
        
        LHS= 0.5*G.node[node]['surplus'] - xE_A_B
        LHS_list.append(LHS)
            #print('LHS= %.5f' % LHS)
    
    sumLHS=sum(x for x in LHS_list)
    # print(sumLHS)
    
    all_patterns=list(product(['0','1'], repeat=len(candidate_dom)))
    for lst_pattern in all_patterns[0:2]:
        pattern=''.join(lst_pattern)
        Fbar, inHandle, notinHandle = add_s_t(F,G,candidate_dom,pattern)

        '''
        print('inHandle:')
        print(inHandle)
        
        print('notinHandle:')
        print(notinHandle)
        '''
        xdeltaH, partitions = nx.minimum_cut(Fbar, 's','t', capacity='weight')
        '''
        print('H:')
        print(partitions[0])
        
        print((inHandle< partitions[0]) or (notinHandle < partitions[0]))
        
        print('x(delta(H))= %.5f' % xdeltaH)
        '''
        
        comb_surplus=xdeltaH + sumLHS
        '''
        print('comb_surplus: %.5f' % comb_surplus)
        print('\n')
        '''
        
        if comb_surplus < comb_upper_bd:
            print('success!!!!!!!!!!!!!!')
            print(partitions[0])
            print('comb surplus: %.5f' % comb_surplus)
            return partitions[0]

    return None
    end=timer()
#    print('running time: %.5f seconds' % (end-start))

if __name__ =='__main__':
    from domgraph import create_dom_graph
    
    F=build_support_graph('pr76.x')
    G=create_dom_graph('pr76.dom', 0.5, 5000)
    for i in range(100000):
        candidate_dom,total_surplus = find_stable_set(G, 0.75)
        find_handle(F,G,candidate_dom,total_surplus, 0.9)

'''
        print('candidate_dom:')
        print(candidate_dom)
        print('total surplus of dominoes: %.5f' %total_surplus)
'''

        
'''
        shrink=shrink_dom_graph(F,G,candidate_dom,pattern)
        Fshrink= shrink[0]
        s=shrink[1]
        t=shrink[2]
        inHandle=shrink[3]
        notinHandle=shrink[4]
        
        cutweight, partitions = nx.minimum_cut(Fshrink, s,t, capacity='weight')
        if cutweight + total_surplus < comb_upper_bd:
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
'''

def find_many_combs(F,G,comb_upper_bd, surplus_bound, ncombs):
    for i in range(ncombs):
        stable=find_stable_set(G,surplus_bound) 
        candidate_dom=stable[0]
        total_surplus=stable[1]
        find_handle(F,G,candidate_dom, total_surplus,comb_upper_bd)
        