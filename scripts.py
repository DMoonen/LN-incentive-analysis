import networkx as nx
import json
import matplotlib.pyplot as plt
import fee_strategies


"""Function that load the data from json from filepath.

:param filepath: The filepath from the root directory one wishes to load the json from.
:returns: The data object present in the json file.
"""
def read_json(file_path):
    with open(file_path, encoding="utf8") as file:
        data = json.load(file)
    file.close()
    return data


"""Function that writes the data to a json file in storage.

:param data: The data object one wishes to write to storage.
:param filepath: The filepath from the root directory one wishes to write the data to.
:returns: void.
"""
def write_json(data, file_path):
    fl = open(file_path, "w")
    json.dump(data, fl)
    fl.close()


"""Function that searches the edge object from a graph object.

:param graph: The graph to search.
:param src_nodes: The node_id of the source.
:param dest_nodes: The node_id of the destination.
:param is_data: Boolean specifying whether the attribute dictionary contained within the edge should be returned.
:returns: Returns the edge if found, -1 otherwise.
"""
def get_edge(graph, src_node, dest_node, is_data):
    try:
        edge_list = graph.edges([src_node], data=is_data)
        for search_candid in edge_list:
            if dest_node == search_candid[1]:
                return search_candid
        return -1
    except:
        print("When attempting to obtain the edge %s -> %s, the search returned an error" % (src_node, dest_node))


"""Function that adds an edge to a given graph.

:param graph: The graph object one wishes to add an edge to.
:param node1: The source of the edge.
:param node2: The destination of the edge.
:param filepath: The weight associated to the edge to be created.
:param needs_optimization: 
:returns: The graph to which an edge has been added.
"""# Todo fix doc
def add_edge(graph, node1, node2, weight, needs_optimization):
    graph.add_edge(node1, node2, weight=weight)
    edge = get_edge(graph, node1, node2, True)
    if needs_optimization:
        graph = fee_strategies.edge_fee_optimization(graph, edge)
    return graph


"""Function that removes an edge from a given graph.

:param graph: The graph object one wishes to remove an edge from.
:param node1: The source of the edge to be removed.
:param node2: The destination of the edge to be removed.
:returns: The graph from which an edge has been removed.
"""
def remove_edge(graph, node1, node2):
    graph.remove_edge(node1, node2)
    graph.remove_edge(node2, node1)
    return graph


"""Function that adds a node to a given graph.

:param graph: The graph object one wishes to add a node to.
:returns: The graph to which a node has been added.
"""
def add_node(graph):
    new_node_id = str(len(graph.nodes()))
    graph.add_node(new_node_id)
    return graph, new_node_id


"""Function that initializes a dictionary that keeps track of the reward each nodes has obtained.
The keys are the nodes, with the value being a list of rewards to keep track of rewards over time.

:param graph: The graph object one wishes to create a reward dictionary for.
:returns: The initialized reward dictionary.
"""
def init_reward_list(graph):
    rewards = {}
    for node in graph.nodes():
        rewards[node] = []
    return rewards


"""Function that calculated the reward obtained by each node in a graph at a given time.
Every node within the network sends a simulated message to each other node. 
The fees of these messages are aggregated by source node for each of the edges, and then stored as the hypothetical 
reward that corresponds to the given graph.

:param graph: The graph object one wishes to calculate the rewards over.
:param prev_rewards: The reward dictionary one wishes to add the rewards to.
:returns: The updated reward dictionary.
"""
def calc_node_profit(graph, prev_rewards):
    for node in graph.nodes():
        prev_rewards[node].append(0)

    between_cent = nx.edge_betweenness_centrality(graph, normalized=False, weight='weight')
    for edge in graph.edges(data=True):
        weight = edge[2]['weight']
        freq_key = (edge[0], edge[1])
        prev_rewards[edge[0]][-1] += between_cent[freq_key] * weight

    return prev_rewards


"""Function creates a plot of the node id's that are present in the node_list.

:param rewards: The reward dictionary.
:param node_list: The list of nodes of which one want the corresponding rewards plotted.
:returns: Void.
"""
def plot_rewards_graph(data_path, rewards, node_list):
    #  xaxis is interval [1, #iterations]
    xaxis = range(1, len(rewards[list(node_list)[0]]) + 1)
    for node in node_list:
        plt.plot(xaxis, rewards[node], label="Node %s" % node)
    plt.xticks(xaxis)
    plt.xlabel('Time (# Iteration)')
    plt.ylabel('Reward (#Milli Satishi\'s)')
    plt.title('Node rewards over time.')
    plt.legend()
    plt.savefig(data_path)
    plt.clf()


"""Function writes the rewards dictionairy as a json file to the requested datapath.

:param rewards: The reward dictionary.
:param data_path: The path to which to write the file to.
:param data_filename: The filename to be written to.
:returns: Void.
"""
def write_rewards_graph_data(rewards, data_path, data_filename):
    write_json(rewards, data_path+data_filename)
    print("Written rewards data to file.")
    return


"""Function that parses a json file to a .gml of a graph object.

:param data_path: Data path from the root of the project folder to the json file.
:param data_filename: The json file name.
:param tx_amts: The fixed transaction size that will be used to calculate the edge weights within the model.
:returns: Void.
"""
def convert_json_to_graph(data_path, data_filename, tx_amts):
    data = read_json(data_path + data_filename)

    key_to_node = {}
    node_to_key = {}

    # Simplify node ID's by map
    pub_keys = [node['pub_key'] for node in data['nodes']]
    node_ids = list(range(0, len(pub_keys)))

    # Fill dictionary maps
    for i in range(0, len(pub_keys)):
        key = pub_keys[i]
        key_to_node[str(key)] = i
        node_to_key[str(i)] = key

    write_json(key_to_node, data_path + "key_to_node_map.json")
    write_json(node_to_key, data_path + "node_to_key_map.json")

    # Parse graph
    for tx_amt in tx_amts:
        print("Starting graph parsing:", tx_amt)
        graph = nx.DiGraph()
        graph.add_nodes_from(node_ids)

        # Convert edges from JSON
        for e in data['edges']:
            u = e['node1_pub']
            v = e['node2_pub']
            node_pol1 = e['node1_policy']
            node_pol2 = e['node2_policy']

            # Make 2 directional edges based on the 2 node policies
            if u in key_to_node and v in key_to_node and node_pol1 is not None:
                fee = int(node_pol1['fee_base_msat']) + int(node_pol1['fee_rate_milli_msat']) * tx_amt * 0.001
                #graph.add_edge(key_to_node[u], key_to_node[v], weight=fee)
                graph = add_edge(graph, key_to_node[u], key_to_node[v], fee, False)

            if u in key_to_node and v in key_to_node and node_pol2 is not None:
                fee = int(node_pol2['fee_base_msat']) + int(node_pol2['fee_rate_milli_msat']) * tx_amt * 0.001
                #graph.add_edge(key_to_node[v], key_to_node[u], weight=fee)
                graph = add_edge(graph, key_to_node[v], key_to_node[u], fee, False)

        nx.write_gml(graph, data_path + "graph" + str(tx_amt) + ".gml")
