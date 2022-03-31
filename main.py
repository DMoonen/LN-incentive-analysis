import networkx as nx
import scripts
import fee_strategies
import placement_strategies

test_flag = 1
node_placement_amt = 4

if test_flag:
    print("testflag enabled!")
    data_path = 'data/testjson/'
    tx_amts = [100, 10000, 1000000]
else:
    data_path = 'data/lnjson/'
    tx_amts = [100, 10000, 1000000]

k2n = scripts.read_json(data_path+"key_to_node_map.json")
n2k = scripts.read_json(data_path+"node_to_key_map.json")

"""" There are 3 scenario's. 
    1. Where it is only us optimizes their solution.
    2. Where us and the network interact may optimize their solution.
    3. Where us and the other party are allowed to optimize their solution.
    4. Where us, the other, and the network are allowed to optimize their solution. 
    
    For each of these scenarios all 6 placement strategies should be tested.
    For each of these scenarios all 3 transaction amount should be tested"""

def scenario1(tx_amt):
    """ Scenario 1 """
    print("Scenario 1")
    # Load the graph
    g = nx.read_gml(data_path+"graph"+str(tx_amt)+".gml")

    # Add a party that represents "us" within the network
    g, our_party_id = scripts.add_node(g)

    # Created the rewards table after all new parties have been created
    rewards = scripts.init_reward_list(g)

    # Allow the network to optimize their fees
    g = fee_strategies.graph_fee_optimization(g)

    # Place the channels
    for node in range(node_placement_amt):
        g = placement_strategies.highest_degree(g, our_party_id, 1)
        rewards = scripts.calc_node_profit(g, rewards)

    # Write to file
    scripts.write_rewards_graph_data(rewards, data_path + "results/", "rewards_highest_degree_" + str(tx_amt)
                                     + "_scenario_1.json")

def scenario2(tx_amt):
    """ Scenario 2 """
    print("Scenario 2")
    # Load the graph
    g = nx.read_gml(data_path+"graph"+str(tx_amt)+".gml")

    # Add a party that represents "us" within the network
    g, our_party_id = scripts.add_node(g)

    # Created the rewards table after all new parties have been created
    rewards = scripts.init_reward_list(g)

    # Allow the network to optimize their fees
    g = fee_strategies.graph_fee_optimization(g)

    # Place the channels
    for node in range(node_placement_amt):
        g = placement_strategies.highest_degree(g, our_party_id, 1)
        rewards = scripts.calc_node_profit(g, rewards)
        g = fee_strategies.graph_fee_optimization(g)

    # Write to file
    scripts.write_rewards_graph_data(rewards, data_path + "results/", "rewards_highest_degree_" + str(tx_amt)
                                     + "_scenario_2.json")

def scenario3(tx_amt):
    """ Scenario 3 """
    print("Scenario 3")
    # Load the graph
    g = nx.read_gml(data_path + "graph" + str(tx_amt) + ".gml")

    # Add a party that represents "us" within the network
    g, our_party_id = scripts.add_node(g)

    # Add a party that represents the channels that will be created after us
    g, other_party_id = scripts.add_node(g)

    # Created the rewards table after all new parties have been created
    rewards = scripts.init_reward_list(g)

    # Allow the network to optimize their fees
    g = fee_strategies.graph_fee_optimization(g)

    # Place the channels
    for node in range(node_placement_amt):
        g = placement_strategies.highest_degree(g, our_party_id, 1)
        rewards = scripts.calc_node_profit(g, rewards)

    # Place other party channels
    for node in range(node_placement_amt):
        g = placement_strategies.highest_degree(g, other_party_id, 1)
        rewards = scripts.calc_node_profit(g, rewards)

    # Write to file
    scripts.write_rewards_graph_data(rewards, data_path + "results/", "rewards_highest_degree_" + str(tx_amt)
                                     + "_scenario_3.json")


def scenario4(tx_amt):
    """ Scenario 4 """
    print("Scenario 4")
    # Load the graph
    g = nx.read_gml(data_path + "graph" + str(tx_amt) + ".gml")

    # Add a party that represents "us" within the network
    g, our_party_id = scripts.add_node(g)

    # Add a party that represents the channels that will be created after us
    g, other_party_id = scripts.add_node(g)

    # Created the rewards table after all new parties have been created
    rewards = scripts.init_reward_list(g)

    # Allow the network to optimize their fees
    g = fee_strategies.graph_fee_optimization(g)

    # Place the channels
    for node in range(node_placement_amt):
        g = placement_strategies.highest_degree(g, our_party_id, 1)
        rewards = scripts.calc_node_profit(g, rewards)
        g = fee_strategies.graph_fee_optimization(g)

    # Place other party channels
    for node in range(node_placement_amt):
        g = placement_strategies.highest_degree(g, other_party_id, 1)
        rewards = scripts.calc_node_profit(g, rewards)
        g = fee_strategies.graph_fee_optimization(g)

    # Write to file
    scripts.write_rewards_graph_data(rewards, data_path + "results/", "rewards_highest_degree_" + str(tx_amt)
                                     + "_scenario_4.json")


for tx_amount in tx_amts:
    print("tx_amt:", tx_amount)
    scenario1(tx_amount)
    scenario2(tx_amount)
    scenario3(tx_amount)
    scenario4(tx_amount)
