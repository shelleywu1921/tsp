from mindomcut3 import build_support_graph, find_handle, add_s_t, del_s_t
from domgraph4 import create_dom_graph2, find_stable_set
from ABcut import edges_cross
from itertools import product
import networkx as nx
from timeit import default_timer as timer

'''
handle_pool = all_handles('att532.pool.txt')

'''
# CONSTANTS:
# F=build_support_graph('att532.x')
# 	it is the support graph of att532.x
# G=create_dom_graph2('att532.dom', teeth_surplus_bound, node_num_upper_bd)
#   G is a graph with no edges. Each node represents a domino whose surplus < teeth_surplus_bound
#   the total number of nodes in G is around node_num_upper_bd
#   For example, G.node[k]['surplus'], G.node[k]['vertices'], G.node[k]['A'], G.node[k]['B']
#   	where k is the k+1 th domino appearing in att532.dom




# for example: all_handles('att532.pool.txt')
# and it produces handle_pool: a set of handles in the handlefilename (e.g. att532.pool.txt)
# Each handle in handle_pool is a frozenset
def all_handles(handlefilename):
    handle_pool = set()
    handlefile=open(handlefilename, 'r')
    first_line=handlefile.readline().split()
    for i in range(int(first_line[1])):
        number_of_node=int(handlefile.readline().split()[0])
        handle_set=frozenset(map(int,handlefile.readline().split()))
        if number_of_node >=3:
            handle_pool.add(handle_set)
    handlefile.close()
    return handle_pool



# the returned value: eligible_teeth, is a nx.Graph()
# its nodes represents teeth in G that respect the handle given. 
# Moreover, eligible_teeth contains all such nodes
# (u,v) is an edge in eligible_teeth iff the dominoes u and v intersect
def find_all_teeth(F, G, handle):
	global newfile
	
	eligible_teeth=nx.Graph()
	for domino in G.nodes():
		A=G.node[domino]['A']
		B=G.node[domino]['B']
		E_A_B=edges_cross(F,A,B)
		xE_A_B=sum(F[u][v]['weight'] for (u,v) in E_A_B)
		#print('find all teeth %.5f' % xE_A_B)
	
		# we only want that teeth if 1/2teethsurplus < x(E(A,B)), not even equality
		if 0.5*G.node[domino]['surplus'] <= xE_A_B -epsilon:
			if (A<= handle and len(B & handle) ==0) or (B<= handle and len(A& handle) ==0):
				eligible_teeth.add_node(domino) #, surplus = G.node[domino]['surplus'],vertices = G.node[domino]['A'].union(G.node[domino]['B']))
	for u in eligible_teeth.nodes():
		for v in eligible_teeth.nodes():
			uteeth = G.node[u]['vertices']
			vteeth= G.node[v]['vertices']
			if (v!=u) and not uteeth.isdisjoint(vteeth):
				eligible_teeth.add_edge(u,v)
	newfile.write(' All eligible teeth for this handle are: \n')
	newfile.write(repr(set(eligible_teeth.nodes())) +' \n')
	newfile.write(' Total number of eligible teeth is: %d \n' % len(list(eligible_teeth.nodes())))

	print('total number of dominoes that can be teeth of the comb is: %d' % len(list(eligible_teeth.nodes())))
	return eligible_teeth


# S is a set()
# x_delta_S computes x(delta(S)) 
def x_delta_S(F, S):
    delta=set()
    for u in S:
        for v in F[u]:
            if (v not in S) and (v != 's') and (v !='t'):
                delta.add((u,v))
    #print('The number of edges in delta is %d' % len(delta))
    delta_weight=sum(F[u][v]['weight'] for (u,v) in delta)
    #print(delta_weight)
    return delta_weight


# find_comb takes F the support graph, G the domino graph, and handle_pool, a set of handles
# for each handle, it finds (at most 100) odd sets of disjoint teeth that respect the handle, 
# then it computes the comb_surplus ( < 1.0 is good) of each comb

def find_comb(F,G,handle_pool):
	global newfile
	
	counter = 0
	viol_comb_set = list()
	for handle in handle_pool:
		newfile.write('\n Handle: \n')
		newfile.write(repr(handle) + '\n')
		
		eligible_teeth=find_all_teeth(F,G,handle)
		if len(list(eligible_teeth.nodes())) >=3:
			for k in range(100): 
				odd_teeth = nx.maximal_independent_set(eligible_teeth) # this is a set
				if len(odd_teeth) >= 3: 
					if len(odd_teeth)%2==0:
						odd_teeth.pop()
					
					newfile.write(' Maximal disjoint teeth set: \n')
					newfile.write(repr(odd_teeth) + '\n')
					print('Number of disjoint teeth: %d' % len(odd_teeth))
					newfile.write(' Number of disjoint teeth: %d \n' % len(odd_teeth))
					
					x_delta_H = x_delta_S(F, handle)
					LHS = x_delta_H + sum(x_delta_S(F,G.node[T]['vertices']) for T in odd_teeth)
					comb_surplus = LHS - 3*len(odd_teeth)
					if comb_surplus < 1: 
						viol_comb = dict()
						viol_comb['handle']=handle
						viol_comb['teeth'] = odd_teeth
						viol_comb['comb_surplus']= comb_surplus
						viol_comb_set.append(viol_comb)
						
						counter +=1
					newfile.write(' comb surplus (<1.0 is good!): %.5f \n\n' % comb_surplus)
					print('comb surplus: %.5f' %comb_surplus)
	newfile.write('total number of violated comb is %d: \n ' % counter)
	newfile.write('And they are: \n ')
	newfile.write(repr(viol_comb_set) + '\n' )
	
	print('total number of violated comb is %d:' % counter)
	print('And they are:')
	print(viol_comb_set)

	return viol_comb_set



if __name__ == "__main__":
	# Variables:
	## creat_dom_graph:
	teeth_surplus_bound = 1.0
	node_num_upper_bd = 50000

	## find_all_teeth:
	epsilon= 0.1     #

	# start:
	start = timer()
	newfilename='from_att532_handlepool_1_1.txt'			# change it every time you run it! 
	newfile=open(newfilename, 'w')
	
	newfile.write('Variables: \n')
	newfile.write('teeth_surplus_bound: %.5f \n' % teeth_surplus_bound)
	newfile.write('node_num_upper_bd: %d \n' % node_num_upper_bd)
	newfile.write('epsilon: %.5f \n' % epsilon)
	
	# constants:
	F=build_support_graph('att532.x')
	G=create_dom_graph2('att532.dom', teeth_surplus_bound, node_num_upper_bd)

	newfile.write('Constants: \n')
	newfile.write('Total number of dominoes: %d \n' % G.number_of_nodes())
	
	handle_pool= all_handles('att532_handlepool_1.txt')
	
	# main function
	viol_comb_set= find_comb(F,G,handle_pool)

	# miscellaneous
	end=timer()
	print('Total running time: %.5f'%(end-start))
	newfile.write('\n Total running time: %.5f'%(end-start))
		


	newfile.close()
    


