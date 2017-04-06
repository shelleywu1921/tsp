'''
I've decided to move the finding comb __name__=='__main__' from mindomcut2.py
to here.

Deleted progreebar, not useful after all. Too lazy to fix it

Moreover, I have added a loop so that the program creates multiple files
'''

from domgraph import create_dom_graph, find_stable_set
from timeit import default_timer as timer
from mindomcut2 import find_handle, build_support_graph



if __name__ =='__main__':
	start=timer()
	
	## VARIABLES ######################################################
	supp_graph_name='att532.x'

	#for create_dom_graph
	domfilename='att532.dom'
	surplus_bound=1.0
	node_num_upper_bound=5000

	#for find_stable_set 
	total_stable_set_surplus_bound=2 # less than 2
	
	#for find_handle
	pattern_upper_bound=130
	comb_upper_bound =1.0   # less than 1
	
	#for the loop
	find_handle_ntimes = 100000  # number of times you want to run findhandle
	####################################################################
	
	F=build_support_graph(supp_graph_name)
	G=create_dom_graph(domfilename, surplus_bound, node_num_upper_bound)
	
	for k in range(1,5): # k=1,2,3,4	
		counter =0 # number of candidate_dom (i.e. number of stable sets) considered
		combs_found=0
		find_handle_nktimes= 10*k

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
		trialname='test_find_handle_'+domfilename.split('.')[0]+ '_'+str(k+3) + '.md'
		trialfile=open(trialname,'w')
		trialfile.write('NOTE: only consider combs with more than 5 teeth! \n')
		trialfile.write('WARNING: comb_upper_bound changed to 1.0! Dont get too excited! \n')		
		trialfile.write(domfilename.split('.')[0]+ '\n')
		trialfile.write('Surplus bound on each domino: %.4f \n' % surplus_bound)
		trialfile.write('Number of nodes in G: %d \n' % G.number_of_nodes())
		trialfile.write('Number of edges in G: %d \n' % G.number_of_edges())
		trialfile.write('Bound on total surplus of stable sets: %.4f \n' % total_stable_set_surplus_bound )
		trialfile.write('Pattern upper bound: %d \n' % pattern_upper_bound)
		trialfile.write('Comb surplus upper bound (<1): %.4f \n' % comb_upper_bound)
		trialfile.write('Running find_handle: %d times \n' % find_handle_nktimes)
		trialfile.write('Number of candidate_dom considered %d \n' % counter)
		trialfile.write('Combs found: %d \n' % combs_found)


		## WRITE COMB ##################################################
		end=timer()
		trialfile.write('Total running time: %.5f seconds' % (end-start))
		trialfile.close()
		print('Total number of sets of candidate_dom considered: %d' % counter)
		print('Combs found: %d \n' % combs_found)
		print('Total time: %.5f seconds' % (end-start))