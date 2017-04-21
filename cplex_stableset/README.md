# April 20 Part 2:
Now using `handle_to_teeth3.3rewrite.py` as the main code. Why not call it `handle_to_teeth3.3.py`? Because `handle_to_teeth3.3.py`'s indentation went wrong and it wouldn't work no matter how I tried to fix it. So in the end I had to rewrite it. 

### What's new about the 3.3 version?

Changed the finding max weight stable function 
```python
from stablesetmip import weighted_stable_set
```
to the finding max weight odd stable set function
```python
from oddstablesetmip import odd_weighted_stable_set
```

### How to create `odd_weight_stable_set`?
Simply adding the constraints 
```
x_1 + ... + x_n = 2z + 1 
z >= 0, integer
```
to the max weight stable set linear model will create turn the function into a max weight odd stable set function. Magical!

Note that the max weight odd set found may only have one node. However, it won't affect the final result. Because if that is the case, then the handle won't have any violated comb.  








# April 20 Part 1:
Start off with everything in `things_that_work/April_18` 

## Modifications:
`handle_to_teeth3.2.py`: This new version of `handle_to_teeth` gives each teeth in `eligible_teeth` a weight, called grwt, which is different from the teeth surplus. 
```python
eligible_teeth.node[domino]['grwt'] = xE_A_B - 0.5* G.node[domino]['surplus'] 
```
It uses 
```python
from stablesetmip import weighted_stable_set
```
to compute a max weight stable set in `eligible_teeth`

Finding odd stable set is still the naive way. If the returned max weight stable set is even, then it pops out the node with the least weight.


## Performances:
### Small examples:
We ran two tests on `att532.handle.test.txt`, first setting `krange=10` then setting `krange=1`. In both tests, it found all handles that have violated combs. When `krange=10`, it returns the same stable set every time.  

However, `test_1.txt` took 17 seconds while `test_2.txt` took 13 seconds. Both are slower than `handle_to_teeth3.1.py`.  

Due to `stablesetmip.py`, it is not necessary to set krange to be more than 1. 

### On fl1577:
First set `krange=10`. For each handle, it returned the same teeth set every time. Thus in the second time we set `krange=1`. It found 9 "violated combs" amonst which 4 are legimately violated. 

Remarkably, the four combs all have different handles. 

In terms of running time, when `krange = 1`, it ran for about 663 seconds, whereas using `htt3.2` on the same setting except `krange=10` ran for 459 seconds. Took a bit longer, but not that much. And it is more efficient in terms of finding handles. 
