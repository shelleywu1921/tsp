We use everything in `things_that_work/April_18` 

# Modifications:
New version of `handle_to_teeth`: `handle_to_teeth3.2.py` gives each teeth in `eligible_teeth` a weight, called grwt, which is different from the teeth surplus. 
```python
eligible_teeth.node[domino]['grwt'] = xE_A_B - 0.5* G.node[domino]['surplus'] 
```

`stablesetmip.py` creates a MIP computing the max weight stable sets given the 


Due to `stablesetmip.py`, it is not necessary to set krange to be more than 1. 
