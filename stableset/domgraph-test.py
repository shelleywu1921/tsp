from __future__ import division

import networkx as nx
from timeit import default_timer as timer


## this is the testing file for domgraph.py
## Testing create_dom_graph and find_stable_set


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
 for i in range(num_of_dom): 
   line=domfile.readline().split()
   surplus=float(line[0])
   if surplus<=surplus_bound:
     Asize=int(line[1]) 
     Bsize=int(line[2])
     A=set(map(int, line[3:3+Asize]))
     B=set(map(int,line[3+Asize:]))
     vertices=set(map(int, line[3:])) 
  
     G.add_node(i, surplus=surplus, Asize=Asize, Bsize=Bsize, A=A, B=B, vertices= vertices)
    
     if G.number_of_nodes()==node_num_upper_bound:
      break
     
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


## testing for create_dom_graph
## passed
'''
def test_create_dom_graph_pr76():
 G=create_dom_graph('pr76.dom',1, 100000)
 assert G.number_of_nodes()==66
 assert G.node[0]['vertices']==set([59,39,40])
 assert G.has_edge(0,1)
 assert not G.has_edge(0,3)
'''

## passed
'''
def test_create_dom_graph_att532():
    G=create_dom_graph('att532.dom',0.5, 5000)
    assert G.number_of_nodes()==5000
    assert G.node[0]['vertices']==set([529,527,528])
    assert G.node[0]['surplus']==0.0006
    assert G.node[0]['Asize']==1
    assert G.node[0]['Bsize']==2
'''


## More_testings

'''
>>> import domgraph as dg
>>> G=dg.create_dom_graph('att532.dom',0.5, 5000)
number of nodes in the graph G: 5000
running time: 97.29837 seconds
>>> G.number_of_edges()
11450125
>>> G.number_of_nodes()
5000

'''




'''
find_stable_set(G, total_surplus_bound) takes a graph G that represents a domfile (i.e. a graph produced by create_dom_graph, and total_surplus_bound, and returns an odd stable set of G and its total surplus (the sum of the surpluses of everything in the odd stable set). Moreover, its total surplus < total_surplus_bound.

Returned value:
    [ listof_candidate_dom, total_surplus]
    listof_candidate_dom is a list of nodes in G
    total_surplus is a float
    
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
  if len(candidate_dom)<3:
      return None
  else:
      return [candidate_dom,total_surplus]

## Testing for find_stable_set
## passed
'''
def test_find_stable_set_pr76():
    G = create_dom_graph('pr76.dom',1, 100000)
    candidate_dom, total_surplus = find_stable_set(G, 0.75)
    assert len(candidate_dom)%2 == 1
    assert total_surplus < 0.75
'''

## another test for pr76
## passed
'''

if __name__ == '__main__':
    start =timer()
    
    G = create_dom_graph('pr76.dom',1, 100000)      # can make changes here
    for i in range(30):                             # can make changes here
        returned_find_stable_set=find_stable_set(G,0.9) # can make changes here
        if returned_find_stable_set != None:
            candidate_dom, total_surplus=returned_find_stable_set
            print('There are %d teeth' % len(candidate_dom))
            print('The teeth are:', candidate_dom)
            for node in candidate_dom:
                surplus=G.node[node]['surplus']
                print('Node %d has surplus: %.5f' %(node, surplus) )
            
            print('Total surplus: %.5f' % total_surplus)
            print('\n')

    end=timer()
    print('running time: %.5f seconds' % (end-start))
'''


## another test for att532
## passed
'''
if __name__ == '__main__':
    start =timer()
    
    G = create_dom_graph('att532.dom',0.5, 5000)      # can make changes here
    for i in range(30):                             # can make changes here
        returned_find_stable_set=find_stable_set(G,0.75) # can make changes here
        if returned_find_stable_set != None:
            candidate_dom, total_surplus=returned_find_stable_set
            print('There are %d teeth' % len(candidate_dom))
            print('The teeth are:', candidate_dom)
            for node in candidate_dom:
                surplus=G.node[node]['surplus']
                print('Node %d has surplus: %.5f' %(node, surplus) )
            
            print('Total surplus: %.5f' % total_surplus)
            print('\n')

    end=timer()
    print('running time: %.5f seconds' % (end-start))
'''


