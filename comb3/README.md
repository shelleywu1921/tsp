# Third Attempt to Find Violated Combs

# April 18
`handle_to_teeth3.1.py` is the code currently in use. Upgraded the data summary in the end of the output file. Also output a file of handles used.   

# April 15

## Descriptions: 
`handle_to_teeth3.py` is the code currently in use. Compared to the older versions `handle_to_teeth.py` and `handle_to_teeth2.py`, it runs wayyyyy faster. This is because  its construction of `G`, the domino graph, uses 

```python
from domgraph4 import create_dom_graph2 
``` 
`create_dom_graph2` is simply a recording of the dominoes and their vertices. Without computing the edges between nodes representing dominoes, it saves a lot of memory, and produces `G` instantly.

## Performance: 
The starting-with-handle method performs surprisingly well on the original handle pool posted, i.e. on `att532.pool.txt`. See `/att532.pool` for the data generated. It went through all 1796  handles in `att532.pool.txt` and all dominoes in `att532.dom` in 40 minutes. Moreover, within two runs of the program, it found 7 distinct violated 3-tooth combs. The code  used is `handle_to_teeth3.py`. 

To repeat the experiment that found violated combs, go to `tsp/things_that_work/April_15` and run 
```bash
$ python handle_to_teeth3.py
```
and it should output a file named `att532_handle_to_teeth_6.txt`.

## Observations:
From looking at the printed value on the screen, all combs found via this method have 3, 5, or 7 teeth. However, only violated 3-tooth combs have been found. 

6 of the 7 violated combs come from the same handle. 

## Variations:  
### Tight combs: 
From the observations, we guess that it is more likely to find violated comb inequalities using handles that are in combs with small surpluses. 

`handle_to_teeth4.py` is a variation of the main code `handle_to_teeth3.py` that is used to test out this idea. Run it on the original handle pool `att532.pool.txt` to produce `att532_handlepool_1.txt`, a file of handles in `att532.pool.txt` which are parts of combs with  surplus <=1.0. The format of the handle file produced is the same as .pool.txt.   


Next, feed the new handle file into `handle_to_teeth3.py`. It produces `from_att532_handlepool_1_1.txt` that records everything. It found 26 violated combs, but they all come from the same handle, which is the handle of the 6 violated combs from above. See the folder `att532_handlepool` for data. 
 

I also manually selected some handles to test. The result is the same as the one above. See `att532.artificial_pool` for data. 
 
### Light cuts as handles:
Finally, I used the firat 1000 light cuts in the .cut file `att532.1.cuts.txt` as handles. The main code's variation to implement this is `handle_to_teeth5.py`. It performed well. Within 20 minutes it found 158 violated combs.  However, it is not known if it is good at finding combs with distinct handles. They all seem to have 3 teeth.    


 



 don't work that well because its construction of `G`, the domino graph, requires 




