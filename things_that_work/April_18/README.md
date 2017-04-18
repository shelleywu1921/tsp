The main code `handle_to_teeth3.1.py` successfully found violated combs in `fl1577.x`.  

## Warning:
Please change the file name on line 208 in `handle_to_teeth3.1.py` 
```python
newfilename='fl1577.pool_100.txt'
```
and make sure it is not a name of an existing file every time you run it. Otherwise, old files may get overwritten. 

### Other parameters in `handle_to_teeth3.1` that you may want to change:
#### Test for a different graph:
The strings  in line 221 and line 222:
```python
F=build_support_graph('fl1577.x')
G=create_dom_graph2('fl1577.dom')
```

The variables from line 191 to line 204:
```python 
teeth_surplus_bound = 1.0
node_num_upper_bd = 50000
handle_num_bound = 2600
x_delta_H_bound = 15
epsilon= 0.1     
krange = 10
```

