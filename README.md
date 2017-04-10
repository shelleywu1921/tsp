# The Travelling Salesman Problem: Finding violated comb inequalities
## Project update, April 10

### Description of the code
I wrote a program to find violated comb inequalities, given x* (e.g. `pr76.x`) and the set of dominoes with surplus < 1 (e.g. `pr76.dom`). 

Call the support graph of x* `F`. The methodology is first constructing a graph `G` where the nodes represent dominoes, and `(u,v)` is an edge in `G` if and only if the dominoes represented by u and v intersect.  Then we run a finding stable sets heuristic on `G` to find an odd stable set. The stable set represents a set of disjoint dominoes in the support  graph `F`. 

To compute a handle for the odd set of disjoint dominoes, we need to decide upon which half of each domino should be inside the handle. This is done by an exhaustive enumeration on all possible ways of assigning halves of dominoes to handles if the number of dominoes is small, and randomly examine possible patterns if the number of dominoes is large.    After knowing which halves are inside the handle and which halves are not, we construct a supergraph of the support graph `F`, called `Fbar`, by adding a node `s` and a node `t` to `F`. `s` and `t` are adjacent to  nodes in the dominoes that are supposed to be inside and outside the handle, respectively. Moreover, the weights of the new edges incident to `s` and `t` are significantly big numbers, say 100.  Compute the min cost s-t cut in `Fbar`. The cut is very unlikely to use any edge incident to `s` or to `t`. (From experiments, the cut weights are usually below 10). Hence, the cut separates the inside-handle halves of the dominoes from the outside-handle halves.    

