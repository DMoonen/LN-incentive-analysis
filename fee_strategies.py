import networkx as nx
import scripts
import numpy as np

ChCost = 10000
div = 10

ebc_global = np.zeros(ChCost + 1)
max_rew_fee = 1
max_rew = 0

print_flag = True


"""Function optimizes the edge fees within a given graph.

:param graph: The graph to be optimized.
:returns: The optimized graph.
"""
def graph_fee_optimization(graph):
    edge_list = graph.edges(data=True)
    for edge in edge_list:
        graph = edge_fee_optimization(graph, edge)
    return graph


"""Function optimizes a single edges' fee within a given graph.

:param graph: The graph object.
:param edge: The edge to be optimized.
:returns: The updated graph.
"""
def edge_fee_optimization(graph, edge):
    src_node = edge[0]
    dest_node = edge[1]
    weight = edge[2]

    reward = edge_fee_calculation(graph, edge)

    print("Optimum Fee: %s" % reward)
    if weight is not reward:
        graph.add_edge(src_node, dest_node, weight=max_rew_fee)

    return graph


"""Function that calculates the optimal fee of an edge within a given graph.

:param graph: The graph object.
:param edge: The edge to be optimized.
:returns: The updated graph.
"""
def edge_fee_calculation(graph, edge):
    global max_rew_fee
    global max_rew
    global ebc_global
    global edge_global

    src_node = edge[0]
    dest_node = edge[1]
    print("Optimizing weight of %s -> %s" % (src_node, dest_node))

    ebc_global = np.zeros(ChCost + 1)
    max_rew_fee = 1
    max_rew = 0

    edge_global = edge
    maximize_channel_reward(graph, 1, ChCost)

    return max_rew_fee


"""Function updates the global variables containing edge betweenness centrality during edge optimalization.

:param graph: The graph object.
:param fee: The fee value to analyse the edge betweenness centrality with.
:returns: The edge betweenness centrality.
"""
def update_ebc(graph, fee):
    src_id = edge_global[0]
    dest_id = edge_global[1]

    graph.add_edge(src_id, dest_id, weight=fee)
    between_cent = nx.edge_betweenness_centrality(graph, normalized=False)
    ebc = between_cent[src_id, dest_id]
    return ebc


"""Function that maximizes channel rewards, by efficiently searching different fee values.
By calculating the maximum theoretical reward for an interval, intervals can be discarded aiding in the search.

:param graph: The graph object.
:param min_fee: Lower bound of the search space.
:param max_fee: Upper bound of the search space.
:returns: Void.
"""
def maximize_channel_reward(graph, min_fee, max_fee):
    global max_rew_fee
    global max_rew
    global ebc_global

    if print_flag:
        print("min_fee = %s" % min_fee)
        print("max_fee = %s" % max_fee)
        print("max_rew = %s" % max_rew)
        print("max_rew_fee = %s" % max_rew_fee)

    er = np.zeros(div)
    er_max = np.zeros(div)

    update_ebc(graph, 1)

    # Base
    if max_fee - min_fee <= 10:
        for fee in np.arange(min_fee, max_fee + 1):
            if ebc_global[fee] == 0:
                ebc = update_ebc(graph, fee)
                ebc_global[fee] = ebc
            else:
                ebc = ebc_global[fee]
            er_local = ebc * fee
            if er_local > max_rew:
                max_rew_fee = fee
                max_rew = er_local
        return

    else:
        if print_flag:
            print("in_recursion")
        # Recursive part
        for index1 in np.arange(0, div):
            fee = int((max_fee - min_fee) * index1 / div) + min_fee
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
            if er[index1] > max_rew:
                max_rew_fee = fee
                max_rew = er[index1]

            er_max[index1] = ebc * (int((max_fee - min_fee) * (index1 + 1) / div) + min_fee)
            if print_flag:
                print("ER_max = %s" % er_max[index1])
            if er[index1] == 0:
                if print_flag:
                    print("break")
                break

        for index1 in np.arange(0, div):

            if er_max[index1] > max_rew:
                rec_min_fee = int((max_fee - min_fee) * index1 / div) + min_fee
                rec_max_fee = int((max_fee - min_fee) * (index1 + 1) / div) + min_fee
                maximize_channel_reward(graph, rec_min_fee, rec_max_fee)
            else:
                rec_min_fee = int((max_fee - min_fee) * index1 / div) + min_fee
                rec_max_fee = int((max_fee - min_fee) * (index1 + 1) / div) + min_fee
                if print_flag:
                    print("discarding: %s - %s" % (rec_min_fee, rec_max_fee))
    return
