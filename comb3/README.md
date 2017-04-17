# Third Attempt to Find Violated Combs

# April 15

## Descriptions: 
`handle_to_teeth3.py` is the code currently in use. Compared to the older versions `handle_to_teeth.py` and `handle_to_teeth2.py`, it runs wayyyyy faster. This is because  its construction of `G`, the domino graph, uses 

```python
from domgraph4 import create_dom_graph2 
``` 
`create_dom_graph2` is simply a recording of the dominoes and their vertices. Without computing the edges between nodes representing dominoes, it saves a lot of memory, and produces `G` instantly.

## Performance: 
The starting-with-handle method performs surprisingly well on the original handle pool posted, i.e. on `att532.pool.txt`. See `/att532.pool` for the data generated. It went through all 1796  handles in `att532.pool.txt` and all dominoes in `att532.dom` in 40 minutes. Moreover, within two runs of the program, it found 7 distinct violated 3-tooth combs. The code  used is `handle_to_teeth3.py`. 

To repeat the same experiment, go to `tsp/things_that_work/April_15` and run 
```bash
$ python handle_to_teeth3.py
```
and it should output a file named `att532_handle_to_teeth_6.txt`.

## Observations:
From looking at the printed data, it seems that all combs found via this method have 3, 5, or 7 teeth. However, only violated 3-tooth combs have been found. 

6 of the 7 violated combs come from the same handle. 

## Variations:  
### Tight combs: 
From the observations, we guess that it is more likely to find violated comb inequalities using handles that are in combs with small surpluses. 

Run `handle_to_teeth4.py` on the original handle pool `att532.pool.txt` to produce `att532_handlepool_1.txt`, a file of handles in `att532.pool.txt` who are parts of combs with  surplus <=1.0. The format of the handle file produced is the same as .pool.txt. Next, feed the new handle file into `handle_to_teeth3.py`. The  



They all come from the same handle!!!


Since from the observation, violated combs usually come from the same handle, I recorded the handles of tight combs (surplus < 1.2) found from the above procedure  and fed them as the handle set to the code, hoping to find violated combs. However, none has been found. See `att532.artificial_pool` for data.   
The handle sets are `att532.artificial_pool.txt` and `att532.artificial_pool2.txt`.

### Light cuts as handles:



 



 don't work that well because its construction of `G`, the domino graph, requires 




# April 15
Currently using `handle_to_teeth3.py`. In this file, the domino graph `G` is created by `create_dom_graph2` in `domgraph4.py`. `create_dom_graph2` *DOES NOT* creat the edges between dominoes. It is essentially just a recording of the nodes. This speeded up the computation significantlly.  For example `att532_handle_to_teeth_4.txt` only took 10 minutes, where as if using handle_to_teeth2.py it would take hours. 


