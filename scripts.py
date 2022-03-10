import networkx as nx
import json
import matplotlib.pyplot as plt


def read_json(file_path):
    with open(file_path) as file:
        data = json.load(file)
    file.close()
    return data


def write_json(data, file_path):
    fl = open(file_path, "w")
    json.dump(data, fl)
    fl.close()


def add_edge(graph, node1, node2, weight):
    graph.add_edge(node1, node2, weight=weight)
    return graph


def remove_edge(graph, node1, node2):
    graph.remove_edge(node1, node2)
    return graph


def add_node(graph):
    new_node_id = str(len(graph.nodes()))
    graph.add_node(new_node_id)
    return graph, new_node_id


def init_reward_list(graph):
    # Initialize a reward list
    rewards = {}
    for node in graph.nodes():
        rewards[node] = []
    return rewards


def calc_node_profit(graph, prev_rewards):
    for node in graph.nodes():
        prev_rewards[node].append(0)

    between_cent = nx.edge_betweenness_centrality(graph, normalized=False, weight='weight')
    for edge in graph.edges(data=True):
        weight = edge[2]['weight']
        freq_key = (edge[0], edge[1])
        prev_rewards[edge[0]][-1] += between_cent[freq_key] * weight

    return prev_rewards


def plot_rewards_graph(rewards, node_list):
    #  xaxis is interval [1, #iterations]
    xaxis = range(1, len(rewards[list(node_list)[0]])+1)
    for node in node_list:
        plt.plot(xaxis, rewards[node], label="Node %s" % node)
    plt.xticks(xaxis)
    plt.xlabel('Time (# Iteration)')
    plt.ylabel('Reward (#Satishi\'s)')
    plt.title('Node rewards over time.')
    plt.legend()
    plt.show()


def convert_json_to_graph(data_path, data_filename, tx_amts):
    data = read_json(data_path+data_filename)

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

    write_json(key_to_node, data_path+"key_to_node_map.json")
    write_json(node_to_key, data_path+"node_to_key_map.json")

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
                graph.add_edge(key_to_node[u],  key_to_node[v], weight=fee)

            if u in key_to_node and v in key_to_node and node_pol2 is not None:
                fee = int(node_pol2['fee_base_msat']) + int(node_pol2['fee_rate_milli_msat']) * tx_amt * 0.001
                graph.add_edge(key_to_node[v],  key_to_node[u], weight=fee)

        nx.write_gml(graph, data_path+"graph"+str(tx_amt)+".gml")


