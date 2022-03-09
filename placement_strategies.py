import networkx as nx
import numpy as np
import scripts

""" Channel creation strategies """


def remove_connected_nodes(nodelist, edgelist, node_id):
    new_connections = list(nodelist)
    new_connections.remove(node_id)  # One is always connected to oneself
    for edge in edgelist:
        # If we find an edge that contains node_id, we remove the other node from new_connections
        if edge[0] == node_id and edge[1] in new_connections:
            new_connections.remove(edge[1])
        elif edge[1] == node_id and edge[0] in new_connections:
            new_connections.remove(edge[0])
    return new_connections


def uniform_random(graph, node_id, n):
    # Filter nodes already connected with
    node_candidates = remove_connected_nodes(graph.nodes(), graph.edges(data=True), node_id)

    # Pick n node(s) our of the new connection
    if n <= len(node_candidates):
        choices = np.random.choice(node_candidates, n, replace=False)
    else:
        choices = np.random.choice(node_candidates, len(node_candidates), replace=False)

    # Add the chosen edges to the network
    for choice in choices:
        graph = scripts.add_edge(graph, node_id, choice, 1000)
        # Todo optimize newly created edge
        # graph = scripts.add_edge(graph, choice, node_id, 1000)
        # Todo optimize newly created edge
    return graph


def highest_degree(graph, node_id, n):
    # Todo
    return graph


def betweenness_centrality(graph, node_id, n):
    # Todo
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
