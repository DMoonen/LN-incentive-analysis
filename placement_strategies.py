import networkx as nx
import numpy as np
import scripts

""" Channel creation strategies """


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


def create_edges(graph, choices, node_id):
    for choice in choices:
        graph = scripts.add_edge(graph, node_id, choice, 1000)
        # Todo optimize newly created edge
        # graph = scripts.add_edge(graph, choice, node_id, 1000)
        # Todo optimize newly created edge
    return graph


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
        if opt_node is not -1:
            graph = create_edges(graph, [opt_node], node_id)

    return graph


def k_center(graph, node_id, n):
    # Todo
    return graph


def k_means(graph, node_id, n):
    # Todo
    return graph


def fee_weighted_centrality(graph, node_id, n):
    # Todo
    return graph
