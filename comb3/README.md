# Third Attempt to Find Violated Combs

# April 17

## `handle_to_teeth3.py`
`handle_to_teeth3.py` is the code currently in use. Compared to the older versions `handle_to_teeth.py` and `handle_to_teeth2.py`, it runs wayyyyy faster. This is because  its construction of `G`, the domino graph, uses 

```python
from domgraph4 import create_dom_graph2 
``` 
### `create_dom_graph2`
`create_dom_graph2` is simply a recording of the dominoes and their vertices. Without computing the edges between nodes representing dominoes, it saves a lot of memory, and produces `G` instantly.

### Performance of   

  

 don't work that well because its construction of `G`, the domino graph, requires 




# April 15
Currently using `handle_to_teeth3.py`. In this file, the domino graph `G` is created by `create_dom_graph2` in `domgraph4.py`. `create_dom_graph2` *DOES NOT* creat the edges between dominoes. It is essentially just a recording of the nodes. This speeded up the computation significantlly.  For example `att532_handle_to_teeth_4.txt` only took 10 minutes, where as if using handle_to_teeth2.py it would take hours. 


