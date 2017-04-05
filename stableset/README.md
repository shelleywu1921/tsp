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