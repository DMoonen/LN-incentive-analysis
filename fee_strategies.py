import networkx as nx
import scripts
import numpy as np

ChCost = 10000
div = 10

ebc_global = np.zeros(ChCost + 1)
maxRewFee = 1
maxRew = 0

print_flag = True

def graph_fee_optimization(graph):
    edge_list = graph.edges(data=True)
    for edge in edge_list:
        graph = edge_fee_optimization(graph, edge)
    return graph


def edge_fee_optimization(graph, edge):
    global maxRewFee
    global maxRew
    global ebc_global
    global edge_global


    src_node = edge[0]
    dest_node = edge[1]
    weight = edge[2]
    print("Optimizing weight of %s -> %s" % (src_node, dest_node))

    ebc_global = np.zeros(ChCost + 1)
    maxRewFee = 1
    maxRew = 0

    edge_global = edge
    maximize_channel_reward(graph, 1, ChCost)

    print("Optimum Fee: %s" % maxRewFee)
    if weight is not maxRewFee:
        graph.add_edge(src_node, dest_node, weight=maxRewFee)

    return graph


def update_ebc(graph, fee):
    src_id = edge_global[0]
    dest_id = edge_global[1]

    graph.add_edge(src_id, dest_id, weight=fee)
    between_cent = nx.edge_betweenness_centrality(graph, normalized=False)
    ebc = between_cent[src_id, dest_id]
    return ebc


def maximize_channel_reward(graph, minFee, maxFee):
    global maxRewFee
    global maxRew
    global ebc_global

    if print_flag:
        print("minFee = %s" % minFee)
        print("maxFee = %s" % maxFee)
        print("maxRew = %s" % maxRew)
        print("maxRewFee = %s" % maxRewFee)

    er = np.zeros(div)
    er_max = np.zeros(div)

    update_ebc(graph, 1)

    # Base
    if maxFee - minFee <= 10:
        for fee in np.arange(minFee, maxFee + 1):
            if ebc_global[fee] == 0:
                ebc = update_ebc(graph, fee)
                ebc_global[fee] = ebc
            else:
                ebc = ebc_global[fee]
            er_local = ebc * fee
            if er_local > maxRew:
                maxRewFee = fee
                maxRew = er_local
        return

    else:
        if print_flag:
            print("in_recursion")
        # Recursive part
        for index1 in np.arange(0, div):
            fee = int((maxFee - minFee) * index1 / div) + minFee
            if print_flag:
                print("f = %s" % fee)

            print(ebc_global[fee])
            if ebc_global[fee] == 0:
                ebc = update_ebc(graph, fee)
                ebc_global[fee] = ebc
            else:
                ebc = ebc_global[fee]

            er[index1] = ebc * fee
            if print_flag:
                print("ebc = %s" % ebc)
                print("ER=", er[index1])
            if er[index1] > maxRew:
                maxRewFee = fee
                maxRew = er[index1]

            # print 'EBC:  ', graph.es[edge.index]['edgebetweenness']
            er_max[index1] = ebc * (((maxFee - minFee) * (index1 + 1) / div) + minFee)
            if print_flag:
                print("ER_max = %s" % er_max[index1])
            if er[index1] == 0:
                if print_flag:
                    print("break")
                break

        for index1 in np.arange(0, div):

            if er_max[index1] > maxRew:
                rec_minFee = int(((maxFee - minFee) * index1 / div) + minFee)
                rec_maxFee = int(((maxFee - minFee) * (index1 + 1) / div) + minFee)
                maximize_channel_reward(graph, rec_minFee, rec_maxFee)
            else:
                rec_minFee = int(((maxFee - minFee) * index1 / div) + minFee)
                rec_maxFee = int(((maxFee - minFee) * (index1 + 1) / div) + minFee)
                if print_flag:
                    print("discarding: %s - %s" % (rec_minFee, rec_maxFee))
    return
