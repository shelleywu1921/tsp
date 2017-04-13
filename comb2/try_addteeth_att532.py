from mimdomcut2 import build_support_graph, find_handle
from domgraph2 import create_dom_graph, find_stable_set
from ABcut import edges_cross
import networkx as nx

'''
Idea: find a light comb inequality, most likely not violated, then try add teeth to the existing inequality.

Test the idea on att532


'''


## Variables:
comb_upper_bd = 1.5
epsilon= 0.1        #
total_surplus_bound = 2 # <=2
pattern_upper_bound = 530
max_teeth_num = 5


## Constants:
F=build_support_graph('att532.x')
G=create_dom_graph('att532.dom')

candidate_dom = find_stable_set(G, total_surplus_bound)


def find_handle2(F,G,candidate_dom,comb_upper_bd,pattern_upper_bound):
    start=timer()
    
    # for each node in candidate_dom, LHS =1/2surplus(Ti)-x*(E(A,B))
    # sumLHS = \sum 1/2 surplus(Ti)-x*(E(Ai,Bi)). Independ on H, the handle chosen
    LHS_list=[]
    print('Number of teeth: %d ' % len(candidate_dom))
    for node in candidate_dom:
        A=G.node[node]['A']
        B=G.node[node]['B']
        
        E_A_B=edges_cross(F,A,B)
        xE_A_B=sum(F[u][v]['weight'] for (u,v) in E_A_B)
        #print('x*(E(A,B))=%.5f' % xE_A_B)
        
        LHS= 0.5*G.node[node]['surplus'] - xE_A_B
        LHS_list.append(LHS)
    
    sumLHS=sum(x for x in LHS_list)
    
    #print(sumLHS)
    
    all_patterns=list(product(['0','1'], repeat=len(candidate_dom)))
    
    if len(all_patterns) < pattern_upper_bound:
    	step =1
    else: 
    	step= math.floor(len(all_patterns)/pattern_upper_bound)
    	
    for i in range(len(all_patterns)):
    	if i%step == 0:
			lst_pattern=all_patterns[i]
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
			'''
			#print('x(delta(H))= %.5f' % xdeltaH)
	
	
			comb_surplus=xdeltaH + sumLHS
			
			print('comb_surplus: %.5f' % comb_surplus)
			
			#print('\n')
			
	
			if comb_surplus < comb_upper_bd:
				print('success!!!!!!!!!!!!!!')
				print(partitions[0])
				print('comb surplus: %.5f' % comb_surplus)
				return partitions[0]
			del_s_t(F)
		
    return None
    end=timer()
    print('running time: %.5f seconds' % (end-start))




def find_all_teeth(F, G, handle):
    eligible_teeth=set()
    for domino in G.nodes():
        A=G.node[domino]['A']
        B=G.node[domino]['B']
        E_A_B=edges_cross(F,A,B)
        xE_A_B=sum(F[u][v]['weight'] for (u,v) in E_A_B)
        
        # we only want that teeth if 1/2teethsurplus < x(E(A,B)), not even equality
        if 0.5*G[domino]['surplus'] <= xE_A_B -0.1:
            if (G[domino]['A']<= handle and len(G[domino]['B']& handle) ==0 or G[domino]['B']<= handle and len(G[domino]['A']& handle) ==0):
                eligible_teeth.add(domino)

    return eligible_teeth


def find_delta_weight(F, node_set):
    delta=set()
    for u in nodes:
        for v in F[u]:
            if v not in nodes:
                delta.add((u,v))
    print('The number of edges in delta is %d' % len(delta))
    delta_weight=sum(graph[u][v]['weight'] for (u,v) in delta)
    return delta_weight



def final_comb_surplus(F, G, handle, eligible_teeth):
    stable_set=nx.maximal_independent_set(G[teeth for teeth in eligible_teeth])
    return find_delta_weight(F, handle) + sum(find_delta_weight(F, teeth) for teeth in stable_set)

if __name__ == "__main__":
    handle = find_handle2(F,G,candidate_dom,comb_upper_bd,pattern_upper_bound)
    find_comb_surplus(F,G, handle)

