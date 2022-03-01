import networkx as nx
import json


def convert_json_to_graph(data_path, data_filename):
    with open(data_path+data_filename) as file:
        data = json.load(file)
    graph = nx.Graph()
    key_to_node = {}
    node_to_key = {}

    # Create a list of all pub_keys in the JSON file.
    pub_keys = [node['pub_key'] for node in data['nodes']]
    # Simplify node ID's
    node_ids = list(range(0, len(pub_keys)))

    # Add simplified node ID's to the graph
    graph.add_nodes_from(node_ids)

    for i in range(0, len(pub_keys)):
        key = pub_keys[i]
        key_to_node[str(key)] = i
        node_to_key[str(i)] = key

    print("Number of Nodes:", graph.number_of_nodes())

    # Convert edges from JSON
    # TODO

    print("Number of Edges:", graph.number_of_edges())

    # Write graph to file
    # TODO

    # Write key_to_node to file
    # TODO

    # Write node_to_key to file
    # TODO
