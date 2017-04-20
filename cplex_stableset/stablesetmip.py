# give a graph graph
from __future__ import print_function


import sys
import cplex
from cplex.exceptions import CplexError
import networkx


# max weight stable set
# return a list of stable set of nodes with maximum weight
def weighted_stable_set(graph):
    # LP Model:
    ## nodes
    graph_obj=[]
    graph_ub=[]
    graph_lb=[]
    graph_ctype = []
    graph_colnames = []
    for node in graph.nodes():
        graph_obj.append(graph.node[node]['grwt'])
        graph_ub.append(1.1) # allow rounding errors
        graph_lb.append(-0.1) # allow rounding errors
        graph_ctype.append('B') # the columns should be binary
        graph_colnames.append('x'+str(node))
    
    ## edges
    graph_rhs=[]
    graph_rownames=[]
    graph_sense=''
    graph_rows=[]
    
    for u,v in graph.edges():
        graph_rhs.append(1.0)
        graph_rownames.append('r'+str(u)+'_'+str(v))
        graph_sense=graph_sense+'L' # in <= form
        graph_rows.append([ ['x'+str(u), 'x'+str(v)], [1.0, 1.0] ])


    # create problem
    prob=cplex.Cplex()
    prob.objective.set_sense(prob.objective.sense.maximize) # maximizing
    prob.variables.add(obj=graph_obj, lb=graph_lb, ub=graph_ub,
                       types=graph_ctype, names=graph_colnames)

    prob.linear_constraints.add(lin_expr=graph_rows, senses=graph_sense,
                                rhs=graph_rhs, names=graph_rownames)

    # solve the problem
    try:
        prob.solve()
    except CplexError as exc:
        print(exc)
        return None


    # print a bunch of stuff:

    print()
    ## solution.get_status() returns an integer code
    print("Solution status = ", prob.solution.get_status(), ":", end=' ')
    ## the following line prints the corresponding string
    print(prob.solution.status[prob.solution.get_status()])
    print("Solution value  = ", prob.solution.get_objective_value())

    numcols = prob.variables.get_num()
    numrows = prob.linear_constraints.get_num()

    slack = prob.solution.get_linear_slacks()
    x = prob.solution.get_values()

#print(slack)
#    print(x)


    for i in len(slack):
        print('Row ' +graph_rownames[i] + ' :  Slack = %10f' % (graph_rownames[i], slack[i]))

    solution_list = []
    for j in len(x):
        print('Column ' +graph_colnames[j] + ' :  Value = %10f' % (graph_colnames[j], x[j]))
        solution_list.append((int(graph_colnames[j][1:]), x[j]))
    print(solution_list)

    # may want to comment this out
    max_indep_set = []
    for node, binary in solution_list:
        if binary >= 0.9:
            max_indep_set.append(node)

    # odd problem:
    '''
    if len(max_indep_set)%2 ==0:
        max_indep_set.sort(key=lambda x: graph.node[x]['grwt'])
        max_indep_set=max_indep_set[1:]
    '''
    return max_indep_set







