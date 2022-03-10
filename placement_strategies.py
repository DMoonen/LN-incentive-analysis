import networkx as nx
import numpy as np
import scripts


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
"""
def create_edges(graph, choices, node_id):
    for choice in choices:
        graph = scripts.add_edge(graph, node_id, choice, 1000)
        # Todo optimize newly created edge
        # graph = scripts.add_edge(graph, choice, node_id, 1000)
        # Todo optimize newly created edge
    return graph


"""Function for determining how to create new edges connecting a node further to the graph.
The strategy used in this function is uniform random. Here every node that creates a new connection is given the same 
change, and one is selected at random.

:param graph: The graph object one wishes to add an edge to.
:param node_id: The source for the edges that need to be created.
:param n: The number of edges that need to be created using this strategy.
:returns: The graph to which edges have been added.
"""
def uniform_random(graph, node_id, n):
    # Filter nodes already connected with
    node_candidates = remove_connected_nodes(graph.nodes(), graph.edges(data=True), node_id)

    # Pick n node(s) our of the new connection
    if n <= len(node_candidates):
        choices = np.random.choice(node_candidates, n, replace=False)
    else:
        choices = np.random.choice(node_candidates, len(node_candidates), replace=False)

    # Add the chosen edges to the network
    graph = create_edges(graph, choices, node_id)
    return graph


"""Function for determining how to create new edges connecting a node further to the graph.
The strategy used in this function is highest degree. Here the nodes that create a new connection are sorted by how many
existing connections they have. Then the top n nodes are chosen to make this connection with.

:param graph: The graph object one wishes to add an edge to.
:param node_id: The source for the edges that need to be created.
:param n: The number of edges that need to be created using this strategy.
:returns: The graph to which edges have been added.
"""
def highest_degree(graph, node_id, n):
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
    graph = create_edges(graph, choices, node_id)
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
"""
def betweenness_centrality(graph, node_id, n):
    # Create n new edges
    for i in range(n):
        # Init of the optimal node to create a connection with
        opt_betweenness = 0
        opt_node = -1

        # Create new connections list.
        node_candidates = remove_connected_nodes(graph.nodes(), graph.edges(data=True), node_id)

        # Try all connections (create, observer, delete)
        for node_candid in node_candidates:
            # Create the candidate edge
            graph = scripts.add_edge(graph, node_id, node_candid, weight=1000)

            # Record the centrality
            between_cent = nx.edge_betweenness_centrality(graph, normalized=False)

            # Store the centrality
            score = between_cent[(node_id, node_candid)]
            if score > opt_betweenness:
                opt_betweenness = score
                opt_node = node_candid

            # Remove the candidate edge
            graph = scripts.remove_edge(graph, node_id, node_candid)

        # Create the optimal betweenness centrality edge
        if opt_node != -1:
            graph = create_edges(graph, [opt_node], node_id)

    return graph


"""Function for determining how to create new edges connecting a node further to the graph.
The strategy used in this function is k-center. Here the aim is to create new channels to shorten the current longest 
path within the network.

:param graph: The graph object one wishes to add an edge to.
:param node_id: The source for the edges that need to be created.
:param n: The number of edges that need to be created using this strategy.
:returns: The graph to which edges have been added.
"""
def k_center(graph, node_id, n):
    # Todo
    return graph


"""Function for determining how to create new edges connecting a node further to the graph.
The strategy used in this function is k-means. Here the aim is to lower the average shortest path within the network.

:param graph: The graph object one wishes to add an edge to.
:param node_id: The source for the edges that need to be created.
:param n: The number of edges that need to be created using this strategy.
:returns: The graph to which edges have been added.
"""
def k_means(graph, node_id, n):
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
"""
def fee_weighted_centrality(graph, node_id, n):
    # Todo
    return graph
