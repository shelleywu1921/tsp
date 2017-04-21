# give a graph graph
from __future__ import print_function


import sys
import cplex
from cplex.exceptions import CplexError
from cplex.exceptions import CplexSolverError
import networkx

'''
populate_oddstablesetmip.py

'''

'''
Note that the odd stable set found may only have one element
'''

# graph here is a dict. graph['nodes'] is a list of [tooth(integer), xdT]
# populate_odd_weighted_stableset(graph)
# only consider stable sets with >= 3 nodes
def populate_odd_weighted_stableset(graph,xdH):
    global eps          # x(delta(H)) for the fixed handle H

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
    except cplex.exceptions.CplexSolverError:
        return None    

    for i in range(prob.solution.pool.get_num()):
        odd_teeth=[eligible_teeth['nodes'][j][0] for j ,x in enumerate(prob.solution.pool.get_values(i)[:-1]) if x ==1.0]
        return prob.solution.pool.get_num()    

    print()
    # solution.get_status() returns an integer code
    print("Solution status = ", c.solution.get_status(), ":", end=' ')
    # the following line prints the corresponding string
    print(c.solution.status[c.solution.get_status()])

    numcols = c.variables.get_num()

    # Print information about the incumbent
    print()
    print("Objective value of the incumbent  = ",
          c.solution.get_objective_value())
    x = c.solution.get_values()
    for j in range(numcols):
        print("Incumbent: Column %d:  Value = %10f" % (j, x[j]))

    # Print information about other solutions
    print()
    numsol = c.solution.pool.get_num()
    print("The solution pool contains %d solutions." % numsol)

    numsolreplaced = c.solution.pool.get_num_replaced()
    print("%d solutions were removed due to the solution pool "
          "relative gap parameter." % numsolreplaced)

    numsoltotal = numsol + numsolreplaced
    print("In total, %d solutions were generated." % numsoltotal)

    meanobjval = c.solution.pool.get_mean_objective_value()
    print("The average objective value of the solutions is %.10g." %
          meanobjval)

    # write out the objective value of each solution and its
    # difference to the incumbent
    names = c.solution.pool.get_names()

    print()
    print("Solution        Objective       Number of variables")
    print("                value           that differ compared to")
    print("                                the incumbent")

    for i in range(numsol):

        objval_i = c.solution.pool.get_objective_value(i)

        x_i = c.solution.pool.get_values(i)

        # compute the number of variables that differ in solution i
        # and in the incumbent
        numdiff = 0
        for j in range(numcols):
            if abs(x_i[j] - x[j]) > epszero:
                numdiff = numdiff + 1
        print("%-15s %-10g      %d / %d" %
              (names[i], objval_i, numdiff, numcols))











    # the two excepts dont really work
    # force z >=1 and try on fl1577
    except CplexError:
        print('ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        return None

    except CplexSolverError:
        print('CPLEX SOLVER ERROR!!!!!!!!!!!')
        return None

    # print a bunch of stuff:
    '''
    print()
    ## solution.get_status() returns an integer code
    print("Solution status = ", prob.solution.get_status(), ":", end=' ')
    ## the following line prints the corresponding string
    print(prob.solution.status[prob.solution.get_status()])
    print("Solution value  = ", prob.solution.get_objective_value())
    '''
    numcols = prob.variables.get_num()
    numrows = prob.linear_constraints.get_num()

    slack = prob.solution.get_linear_slacks()
    x = prob.solution.get_values()

    #print(slack)
    #    print(x)

    '''
    for i in range(len(slack)):
        print('Row ' +graph_rownames[i] + ' :  Slack = %10f' %  slack[i])
    '''

    solution_list = []
    for j in range(len(x)-1):
        print('Column ' +graph_colnames[j] + ' :  Value = %10f' %  x[j])
        solution_list.append((int(graph_colnames[j][1:]), x[j]))
    print('Column z: Value = %10f' % x[-1])

    print(solution_list)

    # may want to comment this out
    max_indep_set = []
    for node, binary in solution_list:
        if binary >= 0.9:
            max_indep_set.append(node)

    # odd problem:

    return max_indep_set







