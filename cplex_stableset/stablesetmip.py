# give a graph graph

import sys
import cplex
from cplex.exceptions import CplexError
import networkx


# max weight stable set
def construct_model(graph):
    obj=[]
    ub=[]
    lb=[]
    
    ctype=['B' for node in graph.nodes()]
    colnames=['x'+str(node) for node in Graph.nodes()]
    rhs=[1.0 for edge in graph.edges()]
    rownames=['r'+str(i) for i in len(graph.edges())]
    sense=''.join(['L' for i in len(graph.edges())])



