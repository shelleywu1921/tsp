import networkx as nx


def build_support_graph(fracsolu):
    
    fracfile=open(fracsolu,'r')
    first_line=map(int,fracfile.readline().split())
    num_of_vertices=first_line[0]
    num_of_edges=first_line[1]
    
    F=nx.Graph()
    for i in range(num_of_edges):
        line=fracfile.readline().split()
        u=int(line[0])
        v=int(line[1])
        edge_wt=float(line[2])
        F.add_nodes_from([u,v])
        F.add_edge(u,v,weight=edge_wt)
    return F



def find_delta_weight(graph,nodes):
    global newfile
    delta=set()
    for u in nodes:
        for v in graph[u]:
            if v not in nodes:
                delta.add((u,v))
    newfile.write('The number of edges in delta is %d \n' % len(delta))
    print('The number of edges in delta is %d' % len(delta))

    delta_weight=sum(graph[u][v]['weight'] for (u,v) in delta)
    newfile.write('x(delta(S))= %.5f \n' % delta_weight)

    print('x(delta(S))= %.5f ' %delta_weight)
    return delta_weight

if __name__=="__main__":
    F=build_support_graph('att532.x')
    comb_filename = 'att532_comb1.txt'
    
    comb_file = open(comb_filename,'r')
    number_of_hyperedges = int(comb_file.readline().split()[0])
    
    newfilename = 'verify_'+ comb_filename
    newfile = open(newfilename,'w')
    
    Handle = set(map(int, comb_file.readline().split()[1:]))
    LHS = find_delta_weight(F, Handle)

    for i in range(number_of_hyperedges-1):
        Ti = set(map(int,comb_file.readline().split()[1:]))
        LHS = LHS + find_delta_weight(F, Ti)

    comb_file.close()
    comb_surplus = LHS - 3*( number_of_hyperedges-1)
    print('comb surplus: %.5f' % comb_surplus)



    newfile.write('comb surplus: %.5f \n' % comb_surplus)
    newfile.close()
