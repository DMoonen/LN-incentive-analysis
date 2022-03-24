import networkx as nx
import scripts
import numpy as np

ChCost = 10000
div = 10


def graph_fee_optimization(graph):
    edge_list = graph.edges(data=True)
    for edge in edge_list:
        graph = edge_fee_optimization(graph, edge)
    return graph


def edge_fee_optimization(graph, edge):
    src_node = edge[0]
    dest_node = edge[1]
    weight = edge[2]
    print("Optimizing weight of %s -> %s" % (src_node, dest_node))

    #if edge[2] < opt_edge[2]:
        #graph.add_edge(opt_edge[0], opt_edge[1], opt_edge[2])

    # if <= options available
        # final iteration

        # Calc highest reward
            # Return

    # else: recursion
        # Divide up into 10 parts
            # Calc the maximum possible (expected) reward
            # If higher than current reward, recursively call this function

    return graph


def maximize_channel_reward(minFee, maxFee):
    return
