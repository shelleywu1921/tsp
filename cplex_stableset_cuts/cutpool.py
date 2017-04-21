from __future__ import division
from timeit import default_timer as timer
import math

'''
cutpool.py
creates a dict() cutpool where cutpool[node]= dict
cutpool[node]['xds'] = x(delta(S))
cutpool[node]['cutset']=frozenset([1,2,3...])

Example:
	create_cutpool('uk49_2c.teeth')
	create_cutpool('uk49_2c.handles')
'''


def create_cutpool(cutfilename, node_num_upper_bound):
	start=timer()
	cutfile=open(cutfilename, 'r')
	firstline=cutfile.readline().split()
	num_of_cut=int(firstline[1])
	
	cutpool=dict()
	'''
	if num_of_cut < cut_num_upper_bound:
		step =1
	else:
		step =math.floor(num_of_cut/cut_num_upper_bound)
	print('step = %d' % step)
	'''

	for i in range(min(num_of_cut, node_num_upper_bound)):
		# if i % step == 0:
		line=cutfile.readline().split()
		xds=float(line[0])
		cutset= frozenset(list(map(int, line[3:])))
		cutpool[i]=dict()
		cutpool[i]['xds']=xds
		cutpool[i]['cutset']=cutset
	
	cutfile.close()
	print('Number of cuts considered: %d' % len(cutpool))
	end=timer()
	print('Total time taken to construct the cutpool: %.5f seconds' % (end-start))
	
	return cutpool		
	
