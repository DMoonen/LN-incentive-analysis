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

k2n = scripts.read_json(data_path+"key_to_node_map.json")
n2k = scripts.read_json(data_path+"node_to_key_map.json")

#print("Base graph")
#print(k2n)
#print(n2k)

"""" There are 3 scenario's. 
    1. Where it is only us optimizes their solution.
    2. Where us and the network interact may optimize their solution.
    3. Where us and the other party are allowed to optimize their solution.
    4. Where us, the other, and the network are allowed to optimize their solution. 
    
    For each of these scenarios all 6 placement strategies should be tested.
    For each of these scenarios all 3 transaction amount should be tested"""

""" Scenario 1 """
g = nx.read_gml(data_path+"graph"+str(tx_amts[0])+".gml")

# Add a party that represents "us" within the network
g, our_party_id = scripts.add_node(g)

# Created the rewards table after all new parties have been created
rewards = scripts.init_reward_list(g)

# Allow the network to optimize their fees
g = fee_strategies.graph_fee_optimization(g)

print("Start placement strategy")
for node in range(node_placement_amt):
    g = placement_strategies.uniform_random(g, our_party_id, node_placement_amt)
    rewards = scripts.calc_node_profit(g, rewards)
print("Added 'our' edges")

scripts.write_rewards_graph_data(rewards, data_path+"results/", "rewards_uniform_random"+str(tx_amts[0])+"base.json")

""" Scenario 2 """
# Add a party that represents the channels that will be created after us
#g, other_party_id = scripts.add_node(g)

# Other party creates new channels
#g = placement_strategies.uniform_random(g, other_party_id, node_placement_amt)
#print("Added 'other' edges")