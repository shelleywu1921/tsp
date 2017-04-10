# The Travelling Salesman Problem: Finding violated comb inequalities
## Project update, April 10

### Next step maybe?


### Description of the code
I wrote a program to find violated comb inequalities, given x* (e.g. `pr76.x`) and the set of dominoes with surplus < 1 (e.g. `pr76.dom`). 

Call the support graph of x* `F`. The methodology is first constructing a graph `G` where the nodes represent dominoes, and `(u,v)` is an edge in `G` if and only if the dominoes represented by u and v intersect.  Then we run a finding stable sets heuristic on `G` to find an odd stable set. The stable set represents a set of disjoint dominoes in the support  graph `F`. 

To compute a handle for the odd set of disjoint dominoes, we need to decide upon which half of each domino should be inside the handle. This is done by an exhaustive enumeration on all possible ways of assigning halves of dominoes to handles if the number of dominoes is small, and randomly examine possible patterns if the number of dominoes is large.    After knowing which halves are inside the handle and which halves are not, we construct a supergraph of the support graph `F`, called `Fbar`, by adding a node `s` and a node `t` to `F`. `s` and `t` are adjacent to  nodes in the dominoes that are supposed to be inside and outside the handle, respectively. Moreover, the weights of the new edges incident to `s` and `t` are significantly big numbers, say 100.  Compute the min cost s-t cut in `Fbar`. The cut is very unlikely to use any edge incident to `s` or to `t`. (From experiments, the cut weights are usually below 10). Hence, the cut separates the inside-handle halves of the dominoes from the outside-handle halves.    

The min cost s-t cut is the handle such that the comb surplus is the smallest give the assignment of which parts should be inside the handle. If the total surplus of the comb using the min cost s-t cut as the handle is < 1, then we find a violated comb! 

### Results on the implementation:
Given x* (e.g. `pr76.x`) and the set of dominoes (e.g. `pr76.dom`), the program first generates k odd sets of disjoint dominoes. (k = 10, 100, 1000, etc). 
Then for each odd set of disjoint dominoes, it computes the best handle for possible arrangements of halves inside and outside the handle.  

We hope that if there exists violated comb inequalities, we will eventually find one by sampling enough combs (i.e. make k large, and sample all possible arrangements).

We break the interval [0,8] to smaller intervals. The program computes possible handles for k odd sets of dominoes, and outputs the number of occurrences of comb surpluses in each interval. 

#### `pr76`: 
Initially, the program only records the number of comb inequalities with surplus < 0.9. As the number of distinct dominoes converge when k becomes large, we tried this on k = 100000 for `pr76`, and claim this to be almost exhaustive. We only considered odd sets with >=5 number of teeth. Unfortunately, it did not find any violated comb. Once we allow the number of teeth to be 3, and record the number of comb inequalities with surplus < 1.0, the program found around 1/10 k violated combs. However, those violations may be caused by rounding errors, since they are around 10^-4 away from 1.




  

  



#### Problems on small graphs (e.g. `pr76`):

#### Problems on large graphs (e.g. `att532`)