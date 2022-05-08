import networkx as nx
import copy
import numpy as np
import multiprocessing
import scripts

ChCost = 10000
div = 10

max_rew_fee = 1
max_rew = 0
edge_global = -1
global_max_rew = 0
global_rewards = np.zeros(ChCost + 1)
edge_global_rew = np.zeros(ChCost + 1)

print_flag = False

"""Function optimizes the edge fees within a given graph.

:param graph: The graph to be optimized.
:returns: The optimized graph.
"""
def graph_fee_optimization(graph):
    calculation_graph = copy.deepcopy(graph)

    available_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(available_cores-2)

    edge_list = graph.edges(data=True)
    new_edges = []

    for edge in edge_list:
        print("Optimizing weight of %s -> %s" % (edge[0], edge[1]))
        result = pool.apply_async(graph_fee_optimization_job, args=(edge, calculation_graph)).get()
        new_edges.append(result)
    pool.close()
    pool.join()
    print(new_edges)
    try:
        for edge in new_edges:
            graph = scripts.add_edge(graph, edge[0], edge[1], edge[2]['weight'], False)
    except:
        if print_flag:
            print("edge not subscriptable")
        pass
    return graph


# Todo documentation
"""Function used for parallelization. It is used to separate the optimization of edge fees into different processes.

:param edge: The edge to be optimized.
:param calculation_graph: The graph to be used during the optimization process.
:returns: A tuple containing the source node, destination node, and the new, more profitable fee. Or nothing if no fee
could be found that is more profitable.
"""
def graph_fee_optimization_job(edge, calculation_graph):
    res = []
    src_node = edge[0]
    dest_node = edge[1]
    weight = edge[2]['weight']

    reward = edge_fee_calculation(calculation_graph, edge)

    if weight is not reward:
        res = (src_node, dest_node, int(reward))
    return res


"""Function optimizes a single edges' fee within a given graph.

:param graph: The graph object.
:param edge: The edge to be optimized.
:returns: The updated graph.
"""
def edge_fee_optimization(graph, edge):
    src_node = edge[0]
    dest_node = edge[1]
    weight = edge[2]['weight']
    print("Optimizing weight of %s -> %s" % (src_node, dest_node))

    max_fee = edge_fee_calculation(graph, edge)

    if print_flag:
        print("Optimum Fee: %s" % max_fee)
    if weight is not max_fee:
        graph = scripts.add_edge(graph, src_node, dest_node, int(max_fee), False)

    return graph


"""Function that computes the reward of the source node of edge_global.
It seperates this into the rewards the edge brings, and the reward that all other connected to the source node bring.

:param fee: The fee value to analyse the rewards with.
:param calculation_graph: The graph object used for the computation.
:returns: edge_rew, rest_rew the rewards respectively.
"""
def compute_node_rew(fee, calculation_graph):
    local_graph = copy.deepcopy(calculation_graph)
    src_node = edge_global[0]
    dest_node = edge_global[1]
    weight = fee

    local_graph = scripts.add_edge(local_graph, src_node, dest_node, weight, False)

    between_cent = nx.edge_betweenness_centrality(local_graph, normalized=False, weight='weight')
    edge_list = local_graph.edges(data=True)
    edge_rew = 0
    rest_rew = 0
    """
        Calculate the total reward of edge_global's source node.
        This is split into edge_rew which constitutes the reward of edge_global, and rest_rew which represents the 
        rewards of all nodes that share the same source but are not edge_global.
    """
    for edge in edge_list:
        if edge[0] == src_node:
            if edge[1] == dest_node:
                edge_rew += weight * between_cent[(src_node, dest_node)]
            else:
                rest_rew += edge[2]['weight'] * between_cent[(src_node, edge[1])]
    return edge_rew, rest_rew


"""Function that calculates the optimal fee of an edge within a given graph.
It does so by trying many values within the search space.

:param graph: The graph object.
:param edge: The edge to be optimized.
:returns: The fee that obtained the highest reward.
"""
def edge_fee_calculation(graph, edge):
    global max_rew_fee
    global max_rew
    global edge_global
    global global_max_rew
    global global_rewards
    global edge_global_rew

    max_rew_fee = 1
    max_rew = 0
    global_rewards = np.zeros(ChCost + 1)
    edge_global_rew = np.zeros(ChCost + 1)

    between_cent = nx.edge_betweenness_centrality(graph, normalized=False, weight='weight')
    edge_list = graph.edges(data=True)
    edge_global = edge

    init_rew = 0
    for e in edge_list:
        if e[0] == edge[0]:
            init_rew += e[2]['weight'] * between_cent[(e[0], e[1])]
    global_max_rew = init_rew

    maximize_channel_reward(graph, 1, ChCost)

    return max_rew_fee


"""Function that maximizes channel rewards, by efficiently searching different fee values.
By calculating the maximum theoretical reward for an interval, intervals can be discarded aiding in the search.

:param graph: The graph object.
:param min_fee: Lower bound of the search space.
:param max_fee: Upper bound of the search space.
:returns: Void. Return is stored in a global variable.
"""
def maximize_channel_reward(graph, min_fee, max_fee):
    global max_rew_fee
    global max_rew
    global global_max_rew
    global global_rewards
    global edge_global_rew

    er = np.zeros(div + 1)
    er_max = np.zeros(div)
    # If the different fee values present, are less then the amount of divisions.
    # Enter the base
    if max_fee - min_fee <= div:
        # For all the fee candidates, calculate the optimal fee
        for fee in np.arange(min_fee, max_fee + 1):
            if global_rewards[fee] == 0:
                e_rew, r_rew = compute_node_rew(fee, graph)
                global_rewards[fee] = e_rew + r_rew

                edge_global_rew[fee] = e_rew

            er_local = global_rewards[fee]
            # If the calculated fee yields a better reward than the current best, replace it.
            if er_local > global_max_rew:
                max_rew_fee = fee
                global_max_rew = er_local
                max_rew = global_max_rew
        return
    # Else/ Recursion
    else:
        # Separate the fee values into divisions
        for index in np.arange(0, div + 1):
            fee = ((max_fee - min_fee) * index // div) + min_fee
            # Compute fee yield
            if global_rewards[fee] == 0:
                e_rew, r_rew = compute_node_rew(fee, graph)
                global_rewards[fee] = e_rew + r_rew

                edge_global_rew[fee] = e_rew

            er[index] = global_rewards[fee]
            # If fee yield is better than current best update
            if er[index] > global_max_rew:
                max_rew_fee = fee
                global_max_rew = er[index]
                max_rew = global_max_rew
            if er[index] == 0:
                break

        # Compute the maximum possible reward for the div
        for index in np.arange(0, div):
            fee = ((max_fee - min_fee) * index // div) + min_fee
            fee_next = ((max_fee - min_fee) * (index + 1) // div) + min_fee
            er_max[index] = (er[index + 1] - edge_global_rew[fee_next]) + (edge_global_rew[fee] * fee_next) // fee

        # Recursively call the interval that contains the highest reward
        for index in np.arange(0, div):
            if er_max[index] > global_max_rew:
                rec_minFee = ((max_fee - min_fee) * index // div) + min_fee
                rec_maxFee = ((max_fee - min_fee) * (index + 1) // div) + min_fee
                maximize_channel_reward(graph, rec_minFee, rec_maxFee)

