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

### Is there anything wrong with my code?
I tried `correctness_test_find_handle_pr76` to test if the code finds ANY violated comb inequality (comb_surplus_bound = 1.0) when the number of teeth is not restricted. 

No comb found, as usual 

### Restrict to only 3 teeth
In `3teeth_test_find_handle_pr76`, we only consider combs with 3 teeth. About 1/10 of total stable sets considered produce violated combs. However, their comb_surplus is fairly close to 1.0. For example, their comb_surplus is like 0.9999 

Now try `3teeth_test_find_handle_att532` for att532. No violated comb

### SET COMB SURPLUS TO `1.5`
You can tell how desparate I am. I am not even looking for violated combs!!!!!!! Well, call those light combs (say comb with surplus 1.5-ish)

`notviol_test_find_handle_att532` :

When the number of teeth is 3, performs pretty well on att532, found a couple of light combs, and was fast too! 

When thhe number of teeth is 5, (I set the upper bound of the number of teeth to be 5, but in most cases they are exactly 5. att532 seems to have large stable sets where each node has a small surplus), the comb surpluses for each (Handle, Teeth) tend to be larger, say 2~5. It still runs pretty fast. 

`CONJECTURE:` based on the observation above, comb surplus for 5-teeth combs are bounded by some 5-ish (5.00042) number. Another observation is that the light combs found have surplus 1.42 ish. Wonder if it implies some structural properties about the graph.

`Reasoning:` I pretty much stared at all numbers printed out

`Next step maybe?`: test  `notviol_test_find_handle_att532` again, but record the number of occurance on each interval, for 3, 5, 7, 9, 11, etc teeth

`WARNING:` Haven't thought about the repetitions of stable sets though.... Will it give us some smart and efficient way to run our code?


## April 7&8

### Record the comb surpluses
The plan is to run test_find_handle_att532. Instead of outputing the number of comb surpluses < some number, we output the number of comb surpluses in different intervals. Test this for 3-teeth combs, 5-teeth combs, 7-teeth combs, etc separately. 

The file `comb_surplus_interval_att532.py` records all comb surpluses generated by find_handle. Now, it also has a loop that calculates the duplications of stable sets generated.
 

`interval_3_att532`: Later, we broke down the intervals 1 ~ 2, 2 ~ 3, and 3~4 to smaller ones to record the behavior. The interval between 2 and 3 has the most number of combs.

`interval_5_att532`: The interval between 3 and 4 has the most number of combs.

`interval_7_att532`: The intervak between 4 and 6, and between 5 and § has the most number of combs


## April 9&10

### fl1577
We computed the 3, 5, 7 teeth intervals for fl1577, like what we did for att532. We will record the performance later, but so far looks like it performs well. For 3 teeth and 5 teeth, it found a couple of violated comb inequalites, which I unfortunately did not record, or got overwritten. Well, will do that later. The difference compared to att532 though, is that we resetted 
```python
    #for create_dom_graph
    surplus_bound=0.5
    node_num_upper_bound=10000

    #for find_stable_set 
    total_stable_set_surplus_bound=1.75
```

I am not sure if this is because the support graph of fl1577 is intrinsically better, or it is due to the setting above. However, to test it out, we are gonna try the above setting for att532. 

#### `interval_3_fl1577`
For k=100 the running time is about 15 minutes. The interval [2,3) has the most comb surpluses. However, we did find 14 violated combs, whose surpluses was unfortunately unrecorded. On the plus side, there are a few combs with surpluses just a bit above 1.0.

#### `interval_5_fl1577`
For k=100 the running time is about 40 minutes. The interval [3,4) and [4,5) have the most comb surpluses. Twice for k=100 the program found 2 violated combs, with surplus 0.992-ish, which could be caused by rounding errors. 
 