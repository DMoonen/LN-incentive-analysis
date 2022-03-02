import networkx as nx
import json


def read_json(file_path):
    with open(file_path) as file:
        data = json.load(file)
    file.close()
    return data


def write_json(data, file_path):
    fl = open(file_path, "w")
    json.dump(data, fl)
    fl.close()


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
        graph = nx.Graph()
        graph.add_nodes_from(node_ids)

        # Convert edges from JSON
        for e in data['edges']:
            u = e['node1_pub']
            v = e['node2_pub']
            node_pol = e['node1_policy']
            if u in key_to_node and v in key_to_node and node_pol is not None:
                fee = int(node_pol['fee_base_msat']) + int(node_pol['fee_rate_milli_msat']) * tx_amt * 0.001
                graph.add_edge(key_to_node[u],  key_to_node[v], weight=fee)

        nx.write_gml(graph, data_path+"graph"+str(tx_amt)+".gml")


