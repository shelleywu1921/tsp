from mindomcut3 import build_support_graph, find_handle, add_s_t, del_s_t
from domgraph2 import create_dom_graph, find_stable_set
from ABcut import edges_cross
from itertools import product
import networkx as nx

'''
handle_pool = all_handles('att532.pool.txt')

'''


# for example: all_handles('att532.pool.txt')
# handle_pool is a set
# each handle in handle_pool is also a set
def all_handles(handlefilename):
    handle_pool = set()
    handlefile=open(handlefilename, 'r')
    first_line=handlefile.readline().split()
    for i in range(int(first_line[1])):
        number_of_node=int(handlefile.readline().split()[0])
        handle_set=set(map(int,handlefile.readline.split()))
        if number_of_node >=3:
            handle_pool.add(handle_set)
    return handle_pool


# eligible_teeth is a graph
def find_all_teeth(F, G, handle):
    eligible_teeth=nx.Graph()
    for domino in G.nodes():
        A=G.node[domino]['A']
        B=G.node[domino]['B']
        E_A_B=edges_cross(F,A,B)
        xE_A_B=sum(F[u][v]['weight'] for (u,v) in E_A_B)
        #print('find all teeth %.5f' % xE_A_B)
        
        # we only want that teeth if 1/2teethsurplus < x(E(A,B)), not even equality
        if 0.5*G.node[domino]['surplus'] <= xE_A_B -epsilon:
            if (G.node[domino]['A']<= handle and len(G.node[domino]['B']& handle) ==0 or G.node[domino]['B']<= handle and len(G.node[domino]['A']& handle) ==0):
                eligible_teeth.add_node(domino, surplus = G.node[domino]['surplus'],vertices = G.node[domino]['vertices'])
    for u in eligible_teeth.nodes():
        for v in eligible_teeth.nodes():
            uteeth =eligible_teeth.node[u]['vertices']
            vteeth=eligible_teeth.node[v]['vertices']
            if (v!=u) and not uteeth.isdisjoint(vteeth):
                eligible_teeth.add_edge(u,v)
    print('total number of dominoes that can be teeth of the comb is: %d' % len(eligible_teeth))
    return eligible_teeth


def x_delta_S(F, S):
    delta=set()
    for u in S:
        for v in F[u]:
            if (v not in S) and (v != 's') and (v !='t'):
                delta.add((u,v))
    print('The number of edges in delta is %d' % len(delta))
    delta_weight=sum(F[u][v]['weight'] for (u,v) in delta)
    print(delta_weight)
    return delta_weight


def find_comb(F,G,handle_pool):
    for handle in handle_pool:
        eligible_teeth=find_all_teeth(F,G,handle)
        odd_teeth = nx.maximal_independent_set(eligible_teeth) # this is a set
        if len(odd_teeth)%2==0:
            odd_teeth.pop()
        print('Number of teeth: %d' % len(odd_teeth))

        x_delta_H = x_delta_S(F, H)
        LHS = x_delta_H + sum(x_delta_S(F,T) for T in odd_teeth)
        comb_surplus = LHS - 3*len(odd_teeth)
        print(comb_surplus)




if __name__ == "__main__":
    ## Variables:
    ## creat_dom_graph:
    teeth_surplus_bound = 0.75
    node_num_upper_bd = 5000

    ## find_all_teeth:
    epsilon= 0.1        #
    '''
    comb_upper_bd = 2.5
    total_surplus_bound = 2 # <=2
    pattern_upper_bound = 530
    max_teeth_num = 5
    '''
    # constants:
    F=build_support_graph('att532.x')
    G=create_dom_graph('att532.dom', teeth_surplus_bound, node_num_upper_bd)
    handle_pool= all_handles('att532.pool.txt')

    find_comb(F,G,handle_pool)


    


