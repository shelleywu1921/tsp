from mindomcut3 import build_support_graph, find_handle, add_s_t, del_s_t
from domgraph4 import create_dom_graph2, find_stable_set
from ABcut import edges_cross
from itertools import product
import networkx as nx
from timeit import default_timer as timer

'''
Things that this new version does: 
	1. add krange, handle_num_bound, x_delta_H_bound as variables
	2. write a more detailed summary to the file. 
	3. Note that in the end, 
	handle_no is not the actual position of the handle in handlepool.txt, b/c some
	handles in the handlepool are not eligible

Major changes made:
	1. handle_pool is now a list of [frozenset, float]
''' 


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
# and it produces handle_pool: a list of handles in the handlefilename (e.g. att532.pool.txt)
# Each handle in handle_pool is a [frozenset, float], where frozenset represents the handle H,
# and float represents x(delta(H))
def all_handles(handlefilename):
	global handle_num_bound, x_delta_H_bound, F

	handle_pool = list()
	handlefile=open(handlefilename, 'r')
	first_line=handlefile.readline().split()
	for i in range(min(int(first_line[1]), handle_num_bound)):
		number_of_node=int(handlefile.readline().split()[0])
		handle_set=frozenset(map(int,handlefile.readline().split()))

		if number_of_node >= 3:
			x_delta_H = x_delta_S(F,handle_set)
			print(x_delta_H)
			if x_delta_H <= x_delta_H_bound:
				handle_pool.append([handle_set, x_delta_H])
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
	global newfile, krange

	counter = 0
	viol_comb_list = list()
	for i in range(len(handle_pool)):
		handle = handle_pool[i][0]
		newfile.write('\n Handle: \n')
		newfile.write(repr(handle) + '\n')
		x_delta_H = handle_pool[i][1]


		eligible_teeth=find_all_teeth(F,G,handle)
		if len(list(eligible_teeth.nodes())) >=3:
			for k in range(krange): 
				odd_teeth = nx.maximal_independent_set(eligible_teeth) # this is a set
				if len(odd_teeth) >= 3: 
					if len(odd_teeth)%2==0:
						odd_teeth.pop()
					
					newfile.write(' Maximal disjoint teeth set: \n')
					newfile.write(repr(odd_teeth) + '\n')
					print('Number of disjoint teeth: %d' % len(odd_teeth))
					newfile.write(' Number of disjoint teeth: %d \n' % len(odd_teeth))
					
					sum_x_delta_Ti = sum(x_delta_S(F,G.node[T]['vertices']) for T in odd_teeth)
					LHS = x_delta_H + sum_x_delta_Ti
					comb_surplus = LHS - 3*len(odd_teeth)
					
					newfile.write('{0:<20}{1:<20}{2:<20}\n'.format('x(delta(H))', 'sum x(delta(Ti))', 'CombSurp'))
					newfile.write('{0:<20}{1:<20}{2:<20}\n\n'.format(x_delta_H, sum_x_delta_Ti, comb_surplus))

					
					# for violated combs
					if comb_surplus < 1: 
						viol_comb = dict()
						#viol_comb['handle']=handle
						viol_comb['handle_no'] = i
						viol_comb['teeth'] = odd_teeth
						viol_comb['x_delta_H']=x_delta_H
						viol_comb['sum_x_delta_Ti']=sum_x_delta_Ti
						viol_comb['comb_surplus']= comb_surplus
						viol_comb_list.append(viol_comb)
						
						counter +=1
						
					#newfile.write(' comb surplus (<1.0 is good!): %.5f \n\n' % comb_surplus)
					print('comb surplus: %.5f' %comb_surplus)
	newfile.write('\ntotal number of violated comb is %d: \n ' % counter)
	newfile.write('And they are: \n')
	for viol_comb in viol_comb_list:
		newfile.write('comb surplus: %.5f \n' % viol_comb['comb_surplus'])
		newfile.write('Handle: ' + repr(handle_pool[viol_comb['handle_no']][0]) + '\n')
		newfile.write('Number of Teeth: %d \n' % len(viol_comb['teeth']))
		newfile.write('Teeth: ' + repr(viol_comb['teeth']) + '\n\n')

	newfile.write('In summary: \n')
	newfile.write('{0:<20}{1:<20}{2:<20}{3:<20}{4:<20}\n'.format('HandleNo', 'NOofTeeth', 
		'x(delta(H))', 'sum x(delta(Ti))', 'CombSurp'))
	for viol_comb in viol_comb_list: 
		newfile.write('{0:<20}{1:<20}{2:<20}{3:<20}{4:<20}\n'.format(viol_comb['handle_no'], 
			len(viol_comb['teeth']), viol_comb['x_delta_H'], viol_comb['sum_x_delta_Ti'], viol_comb['comb_surplus']))


	print('total number of violated comb is %d:' % counter)
	print('And they are:')
	for viol_comb in viol_comb_list:
		print('comb surplus: %.5f ' % viol_comb['comb_surplus'])
		print('Handle: ' + repr(handle_pool[viol_comb['handle_no']][0]))
		print('Number of Teeth: %d' % len(viol_comb['teeth']))
		print('Teeth: ' + repr(viol_comb['teeth']) + '\n')
	
	

	return viol_comb_list



if __name__ == "__main__":
	# Variables:
	## creat_dom_graph:
	teeth_surplus_bound = 1.0
	node_num_upper_bd = 50000

	## all_handles:
	handle_num_bound = 2600
	x_delta_H_bound = 15

	## find_all_teeth:
	epsilon= 0.1     #
	
	## find_comb:
	krange = 10

	# start:
	start = timer()
	newfilename='fl1577.pool_4.txt'			# change it every time you run it! 
	newfile=open(newfilename, 'w')

	
	newfile.write('Variables: \n')
	newfile.write('teeth_surplus_bound: %.5f \n' % teeth_surplus_bound)
	newfile.write('node_num_upper_bd: %d \n' % node_num_upper_bd)
	newfile.write('handle_num_bound: %d \n' % handle_num_bound)
	newfile.write('x_delta_H_bound: %.5f \n' % x_delta_H_bound)
	newfile.write('epsilon: %.5f \n' % epsilon)
	newfile.write('krange: %d \n \n' % krange)
	
	# constants:
	F=build_support_graph('fl1577.x')											# you may need to change this
	G=create_dom_graph2('fl1577.dom', teeth_surplus_bound, node_num_upper_bd)	# you may need to change this 

	newfile.write('Constants: \n')
	newfile.write('Total number of dominoes: %d \n' % G.number_of_nodes())

	handle_pool= all_handles('fl1577.pool.txt')					# you may need to change this
	
	newfile.write('Total number of handles considered: %d \n\n' % len(handle_pool))
	# main function
	viol_comb_list= find_comb(F,G,handle_pool)

	# miscellaneous
	end=timer()
	print('Total running time: %.5f'%(end-start))
	newfile.write('\n Total running time: %.5f'%(end-start))
		
	newfile.close()

	# write to the handle file
	newhandlefilename='handle_'+ newfilename
	newhandlefile = open(newhandlefilename, 'w')

	newhandlefile.write('%d\n'%len(handle_pool))
	for handle, x_delta_H in handle_pool:
		newhandlefile.write( str(x_delta_H) + ' ' + ' '.join(map(str,handle))+ '\n')     

	newhandlefile.close()
