# give a graph graph
from __future__ import print_function


import sys
import cplex
# from cplex.exceptions import CplexError
# from cplex.exceptions import CplexSolverError
# import networkx

'''
populate_oddstablesetmip.py

'''

'''
Note that the odd stable set found may only have one element
'''

# graph here is a dict. graph['nodes'] is a list of [tooth which is an int, xdT]
# populate_odd_weighted_stableset(graph)
# only consider stable sets with >= 3 nodes
def populate_odd_weighted_stableset(graph,xdH):
    global eps          # sum 3-x(d(Ti)) >= x(d(H)) - 1  + eps

    # LP Model:
    ## nodes
    graph_obj=[]
    graph_ub=[]
    graph_lb=[]
    graph_ctype = ''
    graph_colnames = []
    for toothname, xdT in graph['nodes']:
        graph_obj.append(3-xdT)
        graph_ub.append(1.1) # allow rounding errors
        graph_lb.append(-0.1) # allow rounding errors
        graph_ctype=graph_ctype+'B' # the columns should be binary
        graph_colnames.append('x'+str(toothname))
    
    # add the odd constraint: x_1 + ... + x_n = 2z+1
    # or x_1 + ... + x_n -2z = 1
    graph_obj.append(0.0)
    graph_ub.append(cplex.infinity)
    graph_lb.append(0.9) # Want z >=1, allow rounding errors, so that the stable set have at least 3 nodes
    graph_ctype=graph_ctype+'I'
    graph_colnames.append('z')

    ## edges
    graph_rhs=[]
    graph_rownames=[]
    graph_sense=''
    graph_rows=[]
    
    for u,v in graph['edges']:
        graph_rhs.append(1.0)
        graph_rownames.append('r'+str(u)+'_'+str(v))
        graph_sense=graph_sense+'L' # in <= form
        graph_rows.append([ ['x'+str(u), 'x'+str(v)], [1.0, 1.0] ])


    # add the odd constraint: x_1 + ... + x_n = 2z+1
    # or x_1 + ... + x_n -2z = 1
    graph_rhs.append(1.0)
    graph_rownames.append('odd_const_row')
    graph_sense=graph_sense+'E'
    graph_rows.append([ ['x'+str(node) for node in graph.nodes()]+['z'],
                       [1.0 for node in graph.nodes()] + [-2.0]  ])

    # want to populate all solutions such that sum (3-x(d(T))) x_T >= x(d(H)) -1 + eps
    # so add the constraint to the model
    graph_rhs.append(xdH-1+eps)
    graph_rownames.append('viol_row')
    graph_sense=graph_sense+'G' 
    graph_rows.append( [ ['x'+str(toothname) for toothname, xdT in graph['nodes']],
                            [3-xdT for toothname, xdT in graph['nodes']] ])


    # create problem
    prob=cplex.Cplex()
    prob.objective.set_sense(prob.objective.sense.maximize) # maximizing
    prob.variables.add(obj=graph_obj, lb=graph_lb, ub=graph_ub,
                       types=graph_ctype, names=graph_colnames)

    prob.linear_constraints.add(lin_expr=graph_rows, senses=graph_sense,
                                rhs=graph_rhs, names=graph_rownames)

    # solve the problem
    try:
        prob.populate_solution_pool()

    except cplex.exceptions.CplexError as e:
        print(e)
        return None
    except cplex.exceptions.CplexSolverError as e:
        print(e)
        return None    

    for i in range(prob.solution.pool.get_num()):
        odd_teeth=[eligible_teeth['nodes'][j][0] for j ,x in enumerate(prob.solution.pool.get_values(i)[:-1]) if x ==1.0]
        num_of_teeth=len(odd_teeth)
        sum_xdT = sum(eligible_teeth['nodes'][j][1] for j,x in enumerate(prob.solution.pool.get_values(i)[:-1]) if x == 1.0)
        comb_surplus = xdH+sum_xdT-3*num_of_teeth

        newfile.write('Set of Teeth: \n'+ repr(odd_teeth))
        newfile.write('{0:<20}{1:<20}{2:<20}{3:<20}\n'.format('NumofTeeth', 'x(delta(H))', 'sum x(delta(Ti))', 'CombSurp'))
        newfile.write('{0:<20}{1:<20}{2:<20}{3:<20}\n\n'.format(num_of_teeth ,xdH, sum_xdT , comb_surplus))

    newfile.write('\n')
    newfile.write('Total number of violated combs for this handle: %d \n\n' % prob.solution.pool.get_num())

    return prob.solution.pool.get_num()    








