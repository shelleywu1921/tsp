# Finding Stable Sets
this is a description of the functions in this repository.


## A description of `find_handle` in `mindomcut2.py`
Given a comb H, T1, ..., Tk, where k is odd, the comb inequality is violated by x* 
    
    iff x*(delta(H)) + \sum x*(delta(Ti)) < 3k+1

    iff x*(delta(H)) + \sum 1/2 2x*(delta(Ti)) < 3k+1
    
    iff x*(delta(H)) + \sum 1/2 (x*(delta(Ti)) + x*(delta(Ai)) + x*(delta(Bi)) - 2x*(E(Ai,Bi))) < 3k+1

    iff x*(delta(H)) + \sum 1/2( (x*(delta(Ti))-2) + (x*(delta(Ai))-2) + (x*(delta(Bi))-2) ) - x*(E(Ai,Bi)) < 1

    iff x*(delta(H)) + \sum 1/2 surplus(Ti) - x*(E(Ai,Bi)) < 1 


### pr76 performance: meh.
```python
if __name__ =='__main__':
    from domgraph import create_dom_graph
    start=timer()
    F=build_support_graph('pr76.x')
    G=create_dom_graph('pr76.dom', 1.0, 5000)
    
    for i in range(1000):     #Here!             
        find_ss=find_stable_set(G,3)
        if find_ss != None:
            candidate_dom,total_surplus = find_ss
            find_handle(F,G,candidate_dom,total_surplus, 0.9)
    end=timer()
    print('Total time: %.5f seconds' % (end-start))
```

Tried 100 and 1000 for `#Here`. Running time: `44.80712 seconds` and `471.89071 seconds` respectively. `No violated comb found`, unfortunately.

Tried 1 and 10 for att532. Running time: `128.87578 seconds` and `222.66239 seconds` respectively. No violated comb found


## April 5
Brute force to see if there is any violated comb (<0.9) for pr76. 

## April 6
### Tested duplication: 
Test to see how repetitive are the stable sets generated. See `test_repetition.py`. 

`test_duplication_pr76`: The number of unique stable sets tend to 15,000 as the number of iterations tends to infinity. 

`test_duplication_att532`: In constrast, the stable sets found in att532 doesn't have many duplications.

### Finding combs:
At some point, I set comb_upper_bound from 0.9 to 1.0
Created `find_comb_test_pr76.py` and `find_comb_test_att532.py` dedicated to these two examples.

`test_find_handle_att532 1~6`: No combs found. However, noticed that the printed number of teeth for each iteration of find_handle is HUGE: around 9~27

Solution: Modify find_stable_set so that the number of teeth is between 5 to 9

`test_find_handle_pr76`: No combs found either. I wonder if I should all combs to have three teeth.


### Modified `find_stable_set`: Only teeth from 3 to 5 (or 3 to 7, for maybe one example)
Note that for att532, surplus on each domino is `0.75`, and total surplus of stable sets is `1.75`. The graph G is smaller. We set the upper bound of nodes on G to be 5000, but the actual number of nodes is 2446, ish.

Moreover, the comb surplus upper bound is 1.0

`test_duplication_3-5att532`: Since the number of candidate teeth is small, there were a lot of duplications. In the end, 1/10 of the stable sets found are unique. 

`test_find_handle_3-5_att532`: No comb 


