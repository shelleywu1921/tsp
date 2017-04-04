# Finding Stable Sets
this is a description of the functions in this repository.


## A description of `find_handle` in `mindomcut2.py`
Given a comb H, T1, ..., Tk, where k is odd, the comb inequality is violated by x* 
    
    iff x*(delta(H)) + \sum x*(delta(Ti)) < 3k+1

    iff x*(delta(H)) + \sum 1/2 2x*(delta(Ti)) < 3k+1
    
    iff x*(delta(H)) + \sum 1/2 (x*(delta(Ti)) + x*(delta(Ai)) + x*(delta(Bi)) - 2x*(E(Ai,Bi))) < 3k+1

    iff x*(delta(H)) + \sum 1/2( (x*(delta(Ti))-2) + (x*(delta(Ai))-2) + (x*(delta(Bi))-2) ) - x*(E(Ai,Bi)) < 1

    iff x*(delta(H)) + \sum 1/2 surplus(Ti) - x*(E(Ai,Bi)) < 1 


