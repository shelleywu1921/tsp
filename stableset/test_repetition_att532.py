'''
a file dedicated to att532
'''

# test_repetition
'''
So far we've ran find_handle n times, recorded pr76_1 to pr76_7. No violated comb found.
Question: are the same stable sets repeatedly generated?
Now we want to test how repetitive is the random generation of stable sets
'''

from mindomcut2 import find_stable_set, build_support_graph
from domgraph import create_dom_graph
from timeit import default_timer as timer

if __name__=='__main__':
	start=timer()
	## VARIABLES ######################################################
	supp_graph_name='att532.x'

	#for create_dom_graph
	domfilename='att532.dom'
	surplus_bound=0.75
	node_num_upper_bound=5000

	#for find_stable_set 
	total_stable_set_surplus_bound=1.75 # less than 2

	#for the loop: create k files for the largest k in nk  
	find_stable_set_n1times = 100  # number of times you want to run findhandle
	find_stable_set_n2times = 1000
	find_stable_set_n3times = 10000
	####################################################################
	F=build_support_graph(supp_graph_name)
	G=create_dom_graph(domfilename, surplus_bound, node_num_upper_bound)	

	for k in range(1,6): # k=1,2,3
		find_stable_set_nktimes=10**(k)
		without_dup_collection_of_n_stable_sets=set()
		with_dup=0 # count how many stable sets found with duplication
		for i in range(find_stable_set_nktimes):
			find_ss=find_stable_set(G,total_stable_set_surplus_bound) # less than 2
			if find_ss != None:
				with_dup=with_dup+1
				candidate_dom,total_surplus = find_ss
				without_dup_collection_of_n_stable_sets.add(frozenset(candidate_dom))

		without_dup=len(without_dup_collection_of_n_stable_sets)

		## WRITING TO RECORD ###################################################
		# for recording the trial
		trialname='test_duplication_5_'+domfilename.split('.')[0]+ '_'+str(k) + '.md'
		trialfile=open(trialname,'w')
		trialfile.write('NOTE: only consider combs with 5 teeth! \n')
		trialfile.write(domfilename.split('.')[0]+ '\n\n')

		# write duplication
		trialfile.write('With duplicaition, %d stable sets were considered \n' % with_dup)
		trialfile.write('Without duplication, %d stable sets were considered \n' % without_dup)
		trialfile.write('Running find_stable_set: %d times \n\n' % find_stable_set_nktimes)


		trialfile.write('Number of nodes in G: %d \n' % G.number_of_nodes())
		trialfile.write('Number of edges in G: %d \n' % G.number_of_edges())
		trialfile.write('Surplus bound on each domino: %.4f \n' % surplus_bound)
		trialfile.write('Bound on total surplus of stable sets: %.4f \n' % total_stable_set_surplus_bound )

		end=timer()
		trialfile.write('Total running time: %.5f seconds' % (end-start))

		trialfile.close()
		print('With duplicaition, %d stable sets were considered \n' % with_dup)
		print('Without duplicaition, %d stable sets were considered \n' % without_dup)
		print('Total time: %.5f seconds \n \n' % (end-start))
	

