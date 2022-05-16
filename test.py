import networkx as nx
import scripts
import fee_strategies
import placement_strategies

test_flag = 1
node_placement_amt = 1

if test_flag:
    print("testflag enabled!")
    data_path = 'data/testjson/'
    tx_amts = [100, 10000, 1000000]
else:
    data_path = 'data/lnjson/'
    tx_amts = [100, 10000, 1000000]

def test(tx_amt):
    g = nx.read_gml(data_path + "graph" + str(tx_amt) + ".gml")

    # Add a party that represents "us" within the network
    g, our_party_id = scripts.add_node(g)
    g = placement_strategies.highest_degree(g, our_party_id, 2, False)

    # Created the rewards table after all new parties have been created
    rewards = scripts.init_reward_list(g)

    # Place the channels
    for node in range(node_placement_amt):
        g = placement_strategies.k_means(g, our_party_id, 5, True)
        rewards = scripts.calc_node_profit(g, rewards)


if __name__ == '__main__':
    for tx_amount in tx_amts[:1]:
        test(tx_amount)
