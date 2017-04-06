from __future__ import division

import networkx as nx
from timeit import default_timer as timer

import math



'''
create_dom_graph(domfilename, surplus_bound, node_num_upper_bound) takes in domfile, surplus_bound, node_num_upper_bound, and create a graph G whose nodes correspond to the dominoes in domfile. (u,v) is an edge in G, if and only if the dominoes represented by u and v intersect.

    It also prints the running time in seconds

    However, the program stops when the number of eligible nodes in G reaches node_num_upper_bound.
    
Returned value:
    G

Requirements:
    * domfile is a .dom file. see math.uwaterloo.ca/~bico/qss
    * surplus_bound is a float, between 0 and 1. Only dominoes whose surplus <= surplus bound will be considered.
    * node_num_upper_bound: int
    
Example:
create_dom_graph('pr76.dom', 0.5, 5000)

Note:
The best choices for surplus_bound and node_num_upper_bound varies depending on domfile.
'''


def create_dom_graph(domfilename,surplus_bound,node_num_upper_bound):
 start=timer()
 domfile=open(domfilename,'r')
 firstline=domfile.readline().split()
 num_of_dom=int(firstline[1])
 
 G=nx.Graph()
 
 '''
 add the following lines to make the nodes more evenly distributed over the graphs
 '''
 if num_of_dom < node_num_upper_bound:
 	step = 1
 else:
 	step = math.floor(num_of_dom/node_num_upper_bound)
 	print('step= %d' % step)
 	
 for i in range(num_of_dom): 
   line=domfile.readline().split()
   surplus=float(line[0])
   if i % step ==0:
	   if surplus<=surplus_bound:
		 Asize=int(line[1]) 
		 Bsize=int(line[2])
		 A=set(map(int, line[3:3+Asize]))
		 B=set(map(int,line[3+Asize:]))
		 vertices=set(map(int, line[3:])) 
  
	
		 G.add_node(i, surplus=surplus, Asize=Asize, Bsize=Bsize, A=A, B=B, vertices= vertices)
    
   #  if G.number_of_nodes()==node_num_upper_bound:
		#  break
     
 domfile.close()
 print('number of nodes in the graph G: %d' % (G.number_of_nodes()))
  
 for u in G.nodes():
	for v in G.nodes():
	  uteeth =G.node[u]['vertices']
	  vteeth=G.node[v]['vertices']
	  if (v!=u) and not uteeth.isdisjoint(vteeth):
		G.add_edge(u,v)
 print('number of edges in the graph G: %d' % (G.number_of_edges()))
 end=timer()
 print('running time: %.5f seconds' % (end-start)) 
 return G

'''
def save_dom_graph(domfilename, surplus_bound, node_num_upper_bound):
	G=create_dom_graph(domfilename, surplus_bound, node_num_upper_bound)
	graphname= domfilename.split('.')[0] + '_'+ str(surplus_bound) + '_'+ str(node_num_upper_bound)
	nx.write_gexf(G, 'domgraphs/'+graphname)
'''
	
''' 
find_stable_set(G, total_surplus_bound) takes a graph G that represents a domfile (i.e. a graph produced by create_dom_graph, and total_surplus_bound, and returns an odd stable set of G and its total surplus (the sum of the surpluses of everything in the odd stable set). Moreover, its total surplus < total_surplus_bound.

Returned value:
    [ listof_candidate_dom, total_surplus]
    
Requirements:
    * G: a graph produced by create_dom_graph, representing a collection of dominoes
    * total_surplus_bound: a float between 0 and 1
    
Example:
G =create_dom_graph('pr76.dom', 0.5, 5000)
find_stable_set(G, 0.75)

Note:

'''


def find_stable_set(G, total_surplus_bound):
  max_stable_set=nx.maximal_independent_set(G)
  if len(max_stable_set)< 3: 
	return None
  max_stable_set.sort(key=lambda x: G.node[x]['surplus']) 
  first_node=max_stable_set[0]
  candidate_dom =[ first_node ]
  total_surplus=G.node[first_node]['surplus']

  for i in range(1, len(max_stable_set)):
	if i%2 ==1:
	  pass
	else:
	  i_minus_one_node=max_stable_set[i-1]
	  i_node=max_stable_set[i]
	  i_minus_one_surplus=G.node[i_minus_one_node]['surplus']
          i_surplus=G.node[i_node]['surplus']
  
	  if total_surplus + i_minus_one_surplus + i_surplus < total_surplus_bound:
		candidate_dom=candidate_dom+[i_minus_one_node, i_node]
		total_surplus=total_surplus+i_minus_one_surplus+i_surplus
	  else:
		break
	  
	  if len(candidate_dom) ==7:	# up to 7 teeth
	  	break
  if len(candidate_dom)<3:  # changed from 5 to 3
    return None
  else:
    return [candidate_dom,total_surplus]







