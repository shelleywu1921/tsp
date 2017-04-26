from __future__ import division
from timeit import default_timer as timer
import math

'''
cutpool.py
creates a dict() cutpool where cutpool[node]= dict()
cutpool[node]['xds'] = x(delta(S))
cutpool[node]['cutset']=frozenset([1,2,3...])

it records the first min(num_of_cut, node_num_upper_bound) cuts in cutfile

Example:
	create_cutpool('uk49_2c.teeth', 10000)
	create_cutpool('uk49_2c.handles', 10000)
'''


def create_cutpool2(cutfilename, start, node_num_upper_bound):
	start=timer()
	cutfile=open(cutfilename, 'r')
	firstline=cutfile.readline().split()
	num_of_cut=int(firstline[1])

	cutpool=dict()
	for i in range(start):
		cutfile.readline()

	for i in range(start, min(num_of_cut, node_num_upper_bound+start)):
		# if i % step == 0:
		line=cutfile.readline().split()
		xds=float(line[0])
		cutset= frozenset(list(map(int, line[2:])))
		cutpool[i]=dict()
		cutpool[i]['xds']=xds
		cutpool[i]['cutset']=cutset

	cutfile.close()
	print('Number of cuts considered: %d' % len(cutpool))
	end=timer()
	print('Total time taken to construct the cutpool: %.5f seconds' % (end-start))

	return cutpool		
	
