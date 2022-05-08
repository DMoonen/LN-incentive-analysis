import random
import networkx as nx
import fee_strategies

ChCost = 10000

data_path = 'data/testjsonlarge/'
data_filename = 'testjson.json'
tx_amts = [100, 10000, 1000000]

n = 100
p = 1/10

def create_graph(amount):
    temp_g = nx.fast_gnp_random_graph(n, p, directed=True)
    print(temp_g)
    print(temp_g.edges())

    graph = nx.DiGraph()
    graph.add_nodes_from(range(n))
    print(graph)

    for edge in temp_g.edges:
        fee = int(1000 + random.randint(-30, 30) + int(1) * amount * (0.001 + random.uniform(-0.0001, 0.0001)))
        graph.add_edge(edge[0], edge[1], weight=fee)
        graph.add_edge(edge[1], edge[0], weight=fee)

    print(graph.edges(data=True))

    graph = fee_strategies.graph_fee_optimization(graph)

    print(graph.edges(data=True))

    nx.write_gml(graph, data_path + "graph" + str(amount) + ".gml")


if __name__ == '__main__':
    for tx_amount in tx_amts:
        create_graph(tx_amount)
