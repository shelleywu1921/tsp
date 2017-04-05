import networkx as nx
from domgraph import find_stable_set
from itertools import product
from timeit import default_timer as timer
from copy import copy



'''
this takes the support graph of a fract solution and contract every thing in unionA and unionB
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
    Fshrink=nx.MultiGraph(F)
    s=inHandle.pop()
    t=notinHandle.pop()
    
    for vertex in inHandle:
        Fshrink=nx.contracted_nodes(Fshrink,s,vertex, self_loops=False)
    for vertex in notinHandle:
        Fshrink=nx.contracted_nodes(Fshrink,t,vertex, self_loops=False)
    
    return [Fshrink,s,t, inHandle, notinHandle]

def find_handle(F,G,candidate_dom, total_surplus,vio_upper_bd):
    start=timer()
    
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

    all_patterns=list(product([0,1], repeat=len(candidate_dom)))
    for pattern in all_patterns:
        shrink=shrink_dom_graph(F,G,candidate_dom,pattern)
        Fshrink= shrink[0]
        s=shrink[1]
        t=shrink[2]
        inHandle=shrink[3]
        notinHandle=shrink[4]
        
        xdeltaH, partitions = nx.minimum_cut(Fshrink, s,t, capacity='weight')
        print('xdeltaH: %.5f' %xdeltaH)
        comb_surplus=xdeltaH+sumLHS
        
        if comb_surplus< vio_upper_bd:
            end=timer()
            print('success!!!!!!!!!!!!!!')
            print(partitions[0])
            print('comb surplus: %.5f' % comb_surplus)
            return None
            '''
           edge_cut_list=[]
            for p1_node in partitions[0]:
                for p2_node in partitions[1]:
                    if Fshrink.has_edge(p1_node,p2_node):
                        edge_cut_list.append((p1_node,p2_node))
            '''
                

            
            '''
            print('cut weight = %.5f' % cutweight)
            print('total surplus = %.5f' % total_surplus)
            print('cut weight + total surplus = %.5f' % cutweight+total_surplus)
            
            print('running time = %.5f seconds \n'% (end-start))
            '''
    print('Fails :(')
    return None #[cutweight, cutweight+total_surplus, edge_cut_list]
if __name__ =='__main__':
    from domgraph import create_dom_graph
    
    F=build_support_graph('bowtie.x')
    G=create_dom_graph('bowtie.dom', 0.5, 5000)
    for i in range(1):
        candidate_dom,total_surplus = find_stable_set(G, 0.75)
        find_handle(F,G,candidate_dom,total_surplus, 0.9)
            
def find_many_combs(F,G,vio_upper_bd, surplus_bound, ncombs):
    for i in range(ncombs):
        stable=find_stable_set(G,surplus_bound) 
        candidate_dom=stable[0]
        total_surplus=stable[1]
        find_handle(F,G,candidate_dom, total_surplus,vio_upper_bd)
        