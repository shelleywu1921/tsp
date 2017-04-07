'''
This is dedicated to finding combs for att532
From the printed results of test_find_handle_att532 1~6, which were not recorded,
observed that the number of teeth in a stable set tends to be large: around 9~27 (WOW)

'''


# find_com_test.py
'''
I've decided to move the finding comb __name__=='__main__' from mindomcut2.py
to here.

Deleted progreebar, not useful after all. Too lazy to fix it

Moreover, I have added a loop so that the program creates multiple files
'''

from domgraph import create_dom_graph, find_stable_set
from timeit import default_timer as timer
from mindomcut2 import find_handle, build_support_graph

'''
comb_surplus_interval is pretty much like find_handle. However, instead of going through patterns
and stop once it finds a comb with surplus < comb_upper_bound, it goes through all patterns and 
record the comb_surplus for each pattern. 

'''
def comb_surplus_interval(F,G,candidate_dom, total_surplus ,pattern_upper_bound):
    start=timer()
    
    # for each node in candidate_dom, LHS =1/2surplus(Ti)-x*(E(A,B))
    # sumLHS = \sum 1/2 surplus(Ti)-x*(E(Ai,Bi)). Independ on H, the handle chosen
    LHS_list=[]
    print('Number of teeth: %d ' % len(candidate_dom))
    for node in candidate_dom:
        A=G.node[node]['A']
        B=G.node[node]['B']
        
        from ABcut import edges_cross
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
			
			if 0<= comb_surplus < 1:
				0_to_1 +=1
			elif 1<= comb_surplus <2:
				1_to_2+=1
			elif 2<= comb_surplus <3:
				2_to_3+=1
			elif 3<= comb_surplus <4:
				3_to_4+=1
			elif 4<= comb_surplus <5:
				4_to_5+=1
			elif 5<= comb_surplus <6:
				5_to_6+=1
			elif 6<= comb_surplus <7:
				6_to_7+=1				
			elif 7<= comb_surplus <8:
				7_to_8+=1
			else:
				more_than_8+=1																						
			print('comb_surplus: %.5f' % comb_surplus)
			
			#print('\n')
			
			'''
			if comb_surplus < comb_upper_bd:
				print('success!!!!!!!!!!!!!!')
				print(partitions[0])
				print('comb surplus: %.5f' % comb_surplus)
				return partitions[0]
			'''
			
			del_s_t(F)
		
    return None
    end=timer()
    print('running time: %.5f seconds' % (end-start))







if __name__ =='__main__':
	start=timer()
	
	## VARIABLES ######################################################
	supp_graph_name='att532.x'

	#for create_dom_graph
	domfilename='att532.dom'
	surplus_bound=0.75
	node_num_upper_bound=5000

	#for find_stable_set 
	total_stable_set_surplus_bound=1.75 # less than 2
	
	#for find_handle
	pattern_upper_bound=530
	
	#comb_upper_bound =1.5   # less than 1
	

	####################################################################
	
	F=build_support_graph(supp_graph_name)
	G=create_dom_graph(domfilename, surplus_bound, node_num_upper_bound)
	
	for k in range(1,3): # k=1,2
		counter =0 # number of candidate_dom (i.e. number of stable sets) considered
		
		# for the intervals:
		0_to_1 = 0
		1_to_2 = 0
		2_to_3 = 0
		3_to_4 = 0
		4_to_5 = 0
		5_to_6 = 0
		6_to_7 = 0
		7_to_8 = 0
		more_than_8 = 0 
		
		# for the loop		
		find_handle_nktimes= 10**k		# number of times you want to run find_handle

		for i in range(find_handle_nktimes):
			find_ss=find_stable_set(G,total_stable_set_surplus_bound) # less than 2
			if find_ss != None:
				counter=counter+1
				candidate_dom,total_surplus = find_ss
				fh=find_handle(F,G,candidate_dom,total_surplus, comb_upper_bound,pattern_upper_bound)
				if fh !=None:
					combs_found = combs_found+1
					


		## WRITING TO RECORD ###################################################
		# for recording the trial
        
        # PLEASE CHECK THEM!!!!!!!!!!!!!!!!!!!!!!!!!
		trialname='notviol_test_find_handle_5_'+domfilename.split('.')[0]+ '_'+str(k) + '.md'
		trialfile=open(trialname,'w')
		trialfile.write('NOTE: only consider combs 5 teeth! \n')
		trialfile.write('WARNING: comb_upper_bound changed to %.4f! NOT EVEN A VIOLATED COMB! \n' % comb_upper_bound)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
		trialfile.write(domfilename.split('.')[0]+ '\n')
		trialfile.write('Surplus bound on each domino: %.4f \n' % surplus_bound)
		trialfile.write('Number of nodes in G: %d \n' % G.number_of_nodes())
		trialfile.write('Number of edges in G: %d \n' % G.number_of_edges())
		trialfile.write('Bound on total surplus of stable sets: %.4f \n' % total_stable_set_surplus_bound )
        
        #THIS WARNING NOTE MAY NEED SOME CHANGE AS WELL
		trialfile.write('Pattern upper bound: %d. Note: now consider all possible patterns, since number of teeth<=9\n' % pattern_upper_bound)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
		trialfile.write('Comb surplus upper bound: %.4f \n' % comb_upper_bound)
		trialfile.write('Running find_handle: %d times \n' % find_handle_nktimes)
		trialfile.write('Number of candidate_dom considered %d \n' % counter)
		trialfile.write('Combs found: %d \n' % combs_found)


		## WRITE COMB ######################################################################
		
		end=timer()
		trialfile.write('Total running time: %.5f seconds' % (end-start))
		trialfile.close()
		print('Total number of sets of candidate_dom considered: %d' % counter)
		print('Combs found: %d \n' % combs_found)
		print('Total time: %.5f seconds' % (end-start))