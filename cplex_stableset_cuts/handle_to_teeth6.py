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
# the returned value: eligible_teeth, is a dict
# eligible_teeth['nodes'] is a list of [cutname, xdT]
# eligible_teeth['edges'] is a set of tuples (u,v), representing edges, with no repetition
# its nodes represents teeth in teeth_pool that respect the handle given. 
# Moreover, eligible_teeth contains all such nodes
# (u,v) is an edge in eligible_teeth iff the dominoes u and v intersect
def find_all_teeth2(teeth_pool, handleset):
	global newfile
	
	eligible_teeth=dict()
	eligible_teeth['nodes']=list()
	eligible_teeth['edges']=set()
	for tooth in teeth_pool:
		xdT=teeth_pool[tooth]['xds']
		cutset=teeth_pool[tooth]['cutset']
		if (not cutset <= handleset) and (not cutset.isdisjoint(handleset)) :
			eligible_teeth['nodes'].append( [tooth, xdT])
	
	for i in range(len(eligible_teeth['nodes'])):
		for j in range(i, len(eligible_teeth['nodes'])):
			u=eligible_teeth['nodes'][i][0]		# cut number
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

def find_comb(teeth_pool,handle_pool):
	global newfile

	handle_counter=0 # counts the number of handles involving in violated combs
	comb_counter=0 # counts the total number of violated combs found

	for handle in handle_pool:
		xdH=handle_pool[handle]['xds']
		handleset=handle_pool[handle]['cutset']

		if len(handleset) <= 2:
			newfile.write('Handle Number: %d\n' %handle)
			newfile.write('Handle too small, discarded \n\n')
			print('Handle Number: %d' %handle)
			print('Handle too small, discarded')
		else: 
			eligible_teeth=find_all_teeth2(teeth_pool, handleset)
			newfile.write('Handle Number: %d \n' % handle)
			newfile.write('Number of eligible_teeth: %d \n' len(eligible_teeth['nodes']))
			newfile.write('Handle Set: '+repr(handle_pool[handle]['cutset']) + '\n')
			newfile.write('eligible_teeth: ' +repr([tooth for tooth, xdT in eligible_teeth['nodes']]) +'\n\n')
			print('Handle Number: %d' %handle)
			print('Number of eligible_teeth: %d \n' len(eligible_teeth['nodes']))

			if len(eligible_teeth['nodes']) >=3:
				num_viol_combs=populate_odd_weighted_stableset(eligible_teeth,xdH)
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
	'''
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
				odd_teeth = odd_weighted_stable_set(eligible_teeth)
				if odd_teeth !=None and len(odd_teeth) >= 3:

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
	'''


if __name__ == "__main__":
	# Variables:
	# create_cutpool:
	teeth_num_upper_bd = 20000
	handle_num_upper_bd = 1000
	
	## find_comb:
	eps = 0.015

	# start:
	start = timer()
	newfilename='small_uk49_htt6_test_1.txt'			# change it every time you run it!
	newfile=open(newfilename, 'w')

	
	newfile.write('Variables: \n')
	newfile.write('teeth_num_upper_bd: %.5f \n' % teeth_num_upper_bd)
	newfile.write('handle_num_upper_bd: %d \n' % handle_num_upper_bd)
	newfile.write('eps: %.5f \n\n' % eps)
	
	# constants:
	handle_pool=create_cutpool('small_uk49.handles', handle_num_upper_bd)
	teeth_pool=create_cutpool('small_uk49.teeth', teeth_num_upper_bd)


	newfile.write('Constants: \n')
	newfile.write('Total number of handles: %d \n' % len(handle_pool))	
	newfile.write('Total number of teeth: %d \n\n' % len(teeth_pool))

	
	find_comb2(teeth_pool,handle_pool)

	# miscellaneous
	end=timer()
	print('Total running time: %.5f'%(end-start))
	newfile.write('\nTotal running time: %.5f'%(end-start))
		
	newfile.close()

