import networkx as nx
import numpy as np
import scripts
import copy
import multiprocessing


"""Function that takes as input the list of nodes and a node within a graph and removes the id's that are already 
connected. It returns a list of node id's that are not yet connected, from which then the best connection can be 
calculated.

:param nodelist: List of all the node id's within the graph.
:param edgelist: List of all the edges within the graph.
:param node_id: The node id used to determine if a connection is "new" or already existing.
:returns: The list of node id's that will lead to a new connection.
"""
def remove_connected_nodes(nodelist, edgelist, node_id):
    new_connections = list(nodelist)
    new_connections.remove(node_id)  # One is always connected to oneself
    for edge in edgelist:
        # If we find an edge that contains node_id, we ensure that the other node is not present in new_connections
        if edge[0] == node_id and edge[1] in new_connections:
            new_connections.remove(edge[1])
        elif edge[1] == node_id and edge[0] in new_connections:
            new_connections.remove(edge[0])
    return new_connections


"""Function that ads multiple edges to a graph.

:param graph: The graph object one wishes to add an edge to.
:param choices: List of all destinations for which an edge needs to be created.
:param node_id: The source for the edges that need to be created.
:returns: The graph to which edges have been added.
"""# Todo fix doc
def create_edges(graph, choices, node_id, needs_optimization, fee=1000):
    for choice in choices:
        graph = scripts.add_edge(graph, node_id, choice, fee, needs_optimization)
        graph = scripts.add_edge(graph, choice, node_id, fee, needs_optimization)
    return graph


"""Function for determining how to create new edges connecting a node further to the graph.
The strategy used in this function is uniform random. Here every node that creates a new connection is given the same 
change, and one is selected at random.

:param graph: The graph object one wishes to add an edge to.
:param node_id: The source for the edges that need to be created.
:param n: The number of edges that need to be created using this strategy.
:returns: The graph to which edges have been added.
"""# Todo fix doc
def uniform_random(graph, node_id, n, needs_optimization):
    # Filter nodes already connected with
    node_candidates = remove_connected_nodes(graph.nodes(), graph.edges(data=True), node_id)

    # Pick n node(s) our of the new connection
    if n <= len(node_candidates):
        choices = np.random.choice(node_candidates, n, replace=False)
    else:
        choices = np.random.choice(node_candidates, len(node_candidates), replace=False)

    # Add the chosen edges to the network
    graph = create_edges(graph, choices, node_id, needs_optimization)
    return graph


"""Function for determining how to create new edges connecting a node further to the graph.
The strategy used in this function is highest degree. Here the nodes that create a new connection are sorted by how many
existing connections they have. Then the top n nodes are chosen to make this connection with.

:param graph: The graph object one wishes to add an edge to.
:param node_id: The source for the edges that need to be created.
:param n: The number of edges that need to be created using this strategy.
:returns: The graph to which edges have been added.
"""# Todo fix doc
def highest_degree(graph, node_id, n, needs_optimization):
    # Sort by degree
    deg_list = sorted(graph.degree(), key=lambda node: node[1], reverse=True)

    # Map sorted degree list to node id's and filter out the nodes already connected
    node_candidates = remove_connected_nodes([tup[0] for tup in deg_list], graph.edges(data=True), node_id)

    # Pick n node(s) our of the new connection
    if n <= len(node_candidates):
        choices = node_candidates[0:n]
    else:
        choices = node_candidates

    # Add the chosen edges to the network
    graph = create_edges(graph, choices, node_id, needs_optimization)
    return graph


"""Function for determining how to create new edges connecting a node further to the graph.
The strategy used in this function is betweenness centrality. Here the strategy look at all nodes they are currently not
connected with and simulates the creation of an edge with said node. Upon this simulation it is analyzed how many 
transactions would make use of the new channel if every node were to send a simulated message to every other node, and 
the edge with the highest simulated use will be created within the graph.

:param graph: The graph object one wishes to add an edge to.
:param node_id: The source for the edges that need to be created.
:param n: The number of edges that need to be created using this strategy.
:returns: The graph to which edges have been added.
"""# Todo fix doc
def betweenness_centrality(graph, node_id, n, needs_optimization):
    # Record the centrality
    between_cent = nx.betweenness_centrality(graph, normalized=False)
    between_cent_sorted = sorted(between_cent.items(), key=lambda x: x[1], reverse=True)

    # Map sorted degree list to node id's and filter out the nodes already connected
    node_candidates = remove_connected_nodes([tup[0] for tup in between_cent_sorted], graph.edges(data=True), node_id)

    # Pick n node(s) our of the new connection
    if n <= len(node_candidates):
        choices = node_candidates[0:n]
    else:
        choices = node_candidates

    # Add the chosen edges to the network
    graph = create_edges(graph, choices, node_id, needs_optimization)
    return graph


"""Function for determining how to create new edges connecting a node further to the graph.
The strategy used in this function is k-center. Here the aim is to create new channels to shorten the current longest 
path within the network. It aims to do so from the perspective of "our" source node, the closer we are to every other 
node in the network, the closer every other node in the network is to each other (via us).

:param graph: The graph object one wishes to add an edge to.
:param node_id: The source for the edges that need to be created.
:param n: The number of edges that need to be created using this strategy.
:returns: The graph to which edges have been added.
"""
def k_center(graph, node_id, n, needs_optimization):
    for i in range(n):
        dist_dict = nx.single_source_dijkstra_path(graph, node_id)
        dist_dict.pop(node_id)

        longest_path_length = -1
        longest_path_destination = -1
        for path in dist_dict.values():
            if len(path) > longest_path_length and len(path) > 2:
                longest_path_length = len(path)
                longest_path_destination = path[-1]

        if longest_path_destination != -1:
            graph = create_edges(graph, [longest_path_destination], node_id, needs_optimization)
    return graph


"""Function for determining how to create new edges connecting a node further to the graph.
The strategy used in this function is k-means. Here the aim is to lower the average shortest path within the network.

:param graph: The graph object one wishes to add an edge to.
:param node_id: The source for the edges that need to be created.
:param n: The number of edges that need to be created using this strategy.
:returns: The graph to which edges have been added.
"""# Todo fix doc
def k_means(graph, node_id, n, needs_optimization):

    #https://networkx.org/documentation/stable/reference/algorithms/shortest_paths.html
    # average_shortest_path_length?

    # Todo
    return graph


"""Function for determining how to create new edges connecting a node further to the graph.
The strategy used in this function is fee weighted centrality (or greedy). This strategy similar to betweenness 
centrality makes use of the betweenness centrality metric. However this strategy optimizes the weighted fee and edge 
would provide within the simulation, and does not solely rely on the the number of transactions that pass it.

:param graph: The graph object one wishes to add an edge to.
:param node_id: The source for the edges that need to be created.
:param n: The number of edges that need to be created using this strategy.
:returns: The graph to which edges have been added.
"""# Todo fix doc
def fee_weighted_centrality(graph, node_id, n):
    # Create n new edges
    for i in range(n):
        # Create copy for computation
        calculation_graph = copy.deepcopy(graph)

        # Create new connections list.
        node_candidates = remove_connected_nodes(calculation_graph.nodes(), calculation_graph.edges(data=True), node_id)

        # Init multiprocessing
        available_cores = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(available_cores - 2)
        edge_candidates = []

        # Try all possible connections in parallel and store
        for node_candid in node_candidates:
            result = pool.apply_async(fee_weighted_centrality_job, args=(calculation_graph, node_id, node_candid)).get()
            edge_candidates.append(result)

        # Sort list by reward
        edge_candidates.sort(key=lambda y: y[3], reverse=True)

        # If not empty create the edge that yields the highest reward
        if len(edge_candidates) > 0:
            chosen_candid = edge_candidates[0]
            print("Node %s yielded highest reward(fee) with, %d(%d)" % (chosen_candid[1], chosen_candid[3],
                                                                        chosen_candid[2]))
            graph = create_edges(graph, [chosen_candid[1]], chosen_candid[0], False, chosen_candid[2])

    return graph

def fee_weighted_centrality_job(calculation_graph, node_id, node_candid):
    # Create the candidate edge
    calculation_graph = scripts.add_edge(calculation_graph, node_id, node_candid, 1000, True)
    calculation_graph = scripts.add_edge(calculation_graph, node_candid, node_id, 1000, True)

    # Record the centrality
    between_cent = nx.edge_betweenness_centrality(calculation_graph, normalized=False)

    # Calculate the reward
    score = between_cent[(node_id, node_candid)]
    fee = scripts.get_edge(calculation_graph, node_id, node_candid, True)[2]['weight']
    reward = score * fee

    # Remove the candidate edge
    calculation_graph = scripts.remove_edge(calculation_graph, node_id, node_candid)

    res = (node_id, node_candid, fee, reward)
    return res
