# The Travelling Salesman Problem: Finding violated comb inequalities
## Project update, April 10
I wrote programs for finding violated comb inequalities, given x* (e.g. pr76.x) and the set of dominoes with surplus < 1 (e.g. pr76.dom). The methodology of this program is first constructing a graph G where nodes represents dominoes, and (u,v) is an edge if and only if the dominoes represented by u and v interesect.  Then run a finding stable sets heuristic on G to find an odd stable set. Then the stable set represents a set of disjoint dominoes in the support  graph. 
