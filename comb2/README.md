#Second Attempt to Find Violated Combs

In `stableset`, our main approach is to use heuristics to find odd number of disjoint teeth and brute force the best handle. It did not find any violated comb, unfortunately. This time, our approach is to first find the handle, then add teeth to the handle. 


## April 13
Rough idea: first use the `stableset` way to find a (light) comb inequality, then see if we can add teeth to bring the weight down. Let's do this!


