from cutpool import create_cutpool
from itertools import product
from timeit import default_timer as timer

# stableset
from populate_oddstablesetmip import populate_odd_weighted_stableset

'''
Version 6:
1. Changed from optimize to populate to get a family of violated combs 
2. compute the weight 'xdT' directly using 3-x(delta(T))

'''

# teeth_pool is a cutpool. See cutpool.py
# handleset is a frozenset
# the returned value: eligible_teeth, is a dict(), that resembles a graph structure
# eligible_teeth['nodes'] is a list of [cutname, xdT]
# eligible_teeth['edges'] is a set of tuples (u,v), representing edges, with no repetition

# its nodes represents teeth in teeth_pool that respect the handle given. 
# Moreover, eligible_teeth contains all such nodes
# (u,v) is an edge in eligible_teeth iff the dominoes u and v intersect

def find_all_teeth2(teeth_pool, handleset):	
	eligible_teeth=dict()
	eligible_teeth['nodes']=list()
	eligible_teeth['edges']=set()

	for tooth in teeth_pool:
		xdT=teeth_pool[tooth]['xds']
		cutset=teeth_pool[tooth]['cutset']
		if (not cutset <= handleset) and (not cutset.isdisjoint(handleset)) :
			eligible_teeth['nodes'].append( [tooth, xdT] )
	
	for i in range(len(eligible_teeth['nodes'])):
		for j in range(i, len(eligible_teeth['nodes'])):
			u=eligible_teeth['nodes'][i][0]		# cutname
			v=eligible_teeth['nodes'][j][0]
			utooth=teeth_pool[u]['cutset']
			vtooth=teeth_pool[v]['cutset']
			if (v!=u) and not utooth.isdisjoint(vtooth):
				eligible_teeth['edges'].add((u,v))

	print('total number of dominoes that can be teeth of the comb is: %d' % len(eligible_teeth['nodes']))
	return eligible_teeth	




# find_comb takes teeth_pool, a cutpool, and handle_pool, a cutpool,   the domino graph, and handle_pool, a set of handles
# for each handle, it finds (at most 100) odd sets of disjoint teeth that respect the handle, 
# then it computes the comb_surplus ( < 1.0 is good) of each comb

def find_comb2(teeth_pool,handle_pool):
	global newfile

	handle_counter=0 # counts the number of handles involving in violated combs
	comb_counter=0 # counts the total number of violated combs found

	for handle in handle_pool:
		xdH=handle_pool[handle]['xds']
		handleset=handle_pool[handle]['cutset']

		if len(handleset) <= 2:
			newfile.write('Handle Number: %d\n' % handle)
			newfile.write('Handle too small, discarded \n\n')
			print('Handle Number: %d' %handle)
			print('Handle too small, discarded')

		else: 
			eligible_teeth=find_all_teeth2(teeth_pool, handleset)
			newfile.write('Handle Number: %d \n' % handle)
			newfile.write('Number of eligible_teeth: %d \n' % len(eligible_teeth['nodes']))
			newfile.write('Handle Set: '+repr(handle_pool[handle]['cutset']) + '\n')
			newfile.write('eligible_teeth: ' +repr([tooth for tooth, xdT in eligible_teeth['nodes']]) +'\n\n')
			
			print('Handle Number: %d' %handle)
			print('Number of eligible_teeth: %d' % len(eligible_teeth['nodes']))

			if len(eligible_teeth['nodes']) >=3:
				num_viol_combs=populate_odd_weighted_stableset(eligible_teeth,xdH,eps)
				if num_viol_combs != None:
					handle_counter +=1
					comb_counter = comb_counter + num_viol_combs
					print('More violated combs found!!!')
					print('Number of handles that has a violated comb so far: %d' % handle_counter)
					print('Number of violated combs found so far: %d' % comb_counter)

				else:
					newfile.write('No violated comb using this handle is found. \n\n')
					print('No violated comb using this handle is found.')
			else:
				newfile.write('Too few eligible_teeth.\n\n')
				print('Too few eligible_teeth.')

	newfile.write('In summary: \n')
	newfile.write('Number of handles with violated combs: %d \n' % handle_counter)
	newfile.write('Total number of violated combs found: %d \n' % comb_counter)

	return None



if __name__ == "__main__":
	# Variables:
	# create_cutpool:
	teeth_num_upper_bd = 20000
	handle_num_upper_bd = 1000
	
	## find_comb:
	eps = 0.015	 # sum 3-x(d(Ti)) >= x(d(H)) - 1  + eps

	# start:
	start = timer()
	newfilename='small_uk49_htt6_test_1.txt'			# change it every time you run it!
	newfile=open(newfilename, 'w')

	
	newfile.write('Variables: \n')
	newfile.write('teeth_num_upper_bd: %.5f \n' % teeth_num_upper_bd)
	newfile.write('handle_num_upper_bd: %d \n' % handle_num_upper_bd)
	newfile.write('eps: %.5f \n\n' % eps)
	
	# constants:
	handle_pool=create_cutpool('small_uk49.handles', handle_num_upper_bd)	# maybe you want to change this
	teeth_pool=create_cutpool('small_uk49.teeth', teeth_num_upper_bd)		# maybe you want to change this


	newfile.write('Constants: \n')
	newfile.write('Total number of handles: %d \n' % len(handle_pool))	
	newfile.write('Total number of teeth: %d \n\n' % len(teeth_pool))

	
	find_comb2(teeth_pool,handle_pool)

	# miscellaneous
	end=timer()
	print('Total running time: %.5f'%(end-start))
	newfile.write('\nTotal running time: %.5f'%(end-start))
		
	newfile.close()

