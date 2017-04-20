Start off with everything in `things_that_work/April_18` 

# Modifications:
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


# Performances:
## Small examples:
We ran two tests on `att532.handle.test.txt`, first setting `krange=10` then setting `krange=1`. In both tests, it found all handles that have violated combs. When `krange=10`, it returns the same stable set every time.  

However, `test_1.txt` took 17 seconds while `test_2.txt` took 13 seconds. Both are slower than `handle_to_teeth3.1.py`.  

Due to `stablesetmip.py`, it is not necessary to set krange to be more than 1. 
