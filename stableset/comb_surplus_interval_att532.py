'''
This is dedicated to finding combs for att532
From the printed results of test_find_handle_att532 1~6, which were not recorded,
observed that the number of teeth in a stable set tends to be large: around 9~27 (WOW)

'''


'''
comb_surplus_interval is pretty much like find_handle. However, instead of going through patterns
and stop once it finds a comb with surplus < comb_upper_bound, it goes through all patterns and 
record the comb_surplus for each pattern. 
'''

import networkx as nx
from domgraph import create_dom_graph, find_stable_set
from timeit import default_timer as timer
from mindomcut2 import find_handle, build_support_graph
from itertools import product
from mindomcut2 import add_s_t, del_s_t


def comb_surplus_interval(F,G,candidate_dom, total_surplus ,pattern_upper_bound):
    start=timer()
    global zero_to_one, one_to_two, two_to_three, three_to_four, four_to_five, five_to_six, six_to_seven, seven_to_eight, more_than_eight
    
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
				zero_to_one +=1
			elif 1<= comb_surplus <2:
				one_to_two+=1
			elif 2<= comb_surplus <3:
				two_to_three+=1
			elif 3<= comb_surplus <4:
				three_to_four+=1
			elif 4<= comb_surplus <5:
				four_to_five +=1
			elif 5<= comb_surplus <6:
				five_to_six+=1
			elif 6<= comb_surplus <7:
				six_to_seven+=1				
			elif 7<= comb_surplus <8:
				seven_to_eight+=1
			else:
				more_than_eight+=1																						
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
    #print('running time: %.5f seconds' % (end-start))



# find_com_test.py
'''
I've decided to move the finding comb __name__=='__main__' from mindomcut2.py
to here.

Deleted progreebar, not useful after all. Too lazy to fix it

Moreover, I have added a loop so that the program creates multiple files
'''





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
	
	for k in range(1,2): # k=1,2
		counter =0 # number of candidate_dom (i.e. number of stable sets) considered
		
		# for the intervals:
		zero_to_one = 0
		one_to_two = 0
		two_to_three = 0
		three_to_four = 0
		four_to_five = 0
		five_to_six = 0
		six_to_seven = 0
		seven_to_eight = 0
		more_than_eight = 0 
		
		# for the loop		
		find_handle_nktimes= 10**k		# number of times you want to run find_handle

		for i in range(find_handle_nktimes):
			find_ss=find_stable_set(G,total_stable_set_surplus_bound) # less than 2
			if find_ss != None:
				counter=counter+1
				candidate_dom,total_surplus = find_ss
				
				interval=comb_surplus_interval(F,G,candidate_dom, total_surplus ,pattern_upper_bound)
				
				'''
				fh=find_handle(F,G,candidate_dom,total_surplus, comb_upper_bound,pattern_upper_bound)
				if fh !=None:
					combs_found = combs_found+1
				'''	


		## WRITING TO RECORD ###################################################
		# for recording the trial
        
        # PLEASE CHECK THEM!!!!!!!!!!!!!!!!!!!!!!!!!
		trialname='interval_3_'+domfilename.split('.')[0]+ '_'+str(k) + '.md'
		trialfile=open(trialname,'w')
		trialfile.write('Trying patterns for %d candidate doms of size 3. \n' % counter)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
		trialfile.write(domfilename.split('.')[0]+ '\n')
		trialfile.write('Surplus bound on each domino: %.4f \n' % surplus_bound)
		trialfile.write('Number of nodes in G: %d \n' % G.number_of_nodes())
		trialfile.write('Number of edges in G: %d \n' % G.number_of_edges())
		trialfile.write('Bound on total surplus of stable sets: %.4f \n' % total_stable_set_surplus_bound )
        
        #THIS WARNING NOTE MAY NEED SOME CHANGE AS WELL
		trialfile.write('Pattern upper bound: %d. \n Note: now consider all possible patterns, since number of teeth<=9\n' % pattern_upper_bound)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
		trialfile.write('Running comb_surplus_interval: %d times \n' % find_handle_nktimes)
		trialfile.write('Number of candidate_dom considered %d \n \n' % counter)


        # interval recording
        trialfile.write('Comb surpluses: \n')
        trialfile.write('0 <= comb_surplus < 1:{0:10} \n'.format(zero_to_one))
        trialfile.write('1 <= comb_surplus < 2:{0:10} \n'.format(one_to_two))
        trialfile.write('2 <= comb_surplus < 3:{0:10} \n'.format(two_to_three))
        trialfile.write('3 <= comb_surplus < 4:{0:10} \n'.format(three_to_four))
        trialfile.write('4 <= comb_surplus < 5:{0:10} \n'.format(four_to_five))
        trialfile.write('5 <= comb_surplus < 6:{0:10} \n'.format(five_to_six))
        trialfile.write('6 <= comb_surplus < 7:{0:10} \n'.format(six_to_seven))
        trialfile.write('7 <= comb_surplus < 8:{0:10} \n'.format(seven_to_eight))
        trialfile.write('>= 8:{0:27} \n'.format(more_than_eight))
    

		## WRITE COMB ######################################################################
		
        end=timer()
        trialfile.write('Total running time: %.5f seconds' % (end-start))
        trialfile.close()
        print('Total number of sets of candidate_dom considered: %d' % counter)

        #print('Combs found: %d \n' % combs_found)

        print('Total time: %.5f seconds' % (end-start))






