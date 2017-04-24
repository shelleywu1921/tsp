def x_delta_S(F, S):
    delta=set()
    for u in S:
        for v in F[u]:
            if (v not in S) and (v != 's') and (v !='t'):
                delta.add((u,v))
    #print('The number of edges in delta is %d' % len(delta))
    delta_weight=sum(F[u][v]['weight'] for (u,v) in delta)
    print(delta)
    #print(delta_weight)
    return delta_weight