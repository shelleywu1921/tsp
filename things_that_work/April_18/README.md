The main code `handle_to_teeth3.1.py` successfully found violated combs in `fl1577.x`.  

## Warning:
Please change the file name on line 208 in `handle_to_teeth3.1.py` 
```python
newfilename='fl1577.pool_100.txt'
```
and make sure it is not a name of an existing file every time you run it. Otherwise, old files may get overwritten. 

### Other parameters in `handle_to_teeth3.1.py` that you may want to change:
If you want to use it on a different graph, change the file names on line 221, 222, and 227:
```python
F=build_support_graph('fl1577.x')                   # support graph file
G=create_dom_graph2('fl1577.dom')                   # domino file
handle_pool= all_handles('fl1577.pool.txt')	        # handle pool file
```

Changing the following variables from from line 191 to line 204 may yield different results!
```python 
teeth_surplus_bound = 1.0     # only dominoes with surpluses < t_s_b will be considered. 
                              # Setting it =1.0 means considering all doms
node_num_upper_bd = 50000     # only use about n_n_u_b dominoes from the .dom file
handle_num_bound = 2600       # only use at most h_n_b handles  
x_delta_H_bound = 15          # only handles with x(delta(H)) <= x_d_H_b will be considered as a candidate handle
epsilon= 0.1                  # for each handle and all teeth that respects it, only consider those with 
                              # 1/2*teeth_surplus < x(E(A:B)) - epsilon
krange = 10                   # for each handle and a set of teeth that respects it, run odd stable set 
                              # heuristics and compute the comb surpluses krange times. (This is because 
                              # that the heuristic may yield a different result each time)
```

## A small example for testing:
Input the following on line 221, 222, and 227:
```python
F=build_support_graph('att532.x')
G=create_dom_graph2('att532.dom')
handle_pool= all_handles('att532.pool.test.txt')	
```
