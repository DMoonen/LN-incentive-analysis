import networkx as nx
import scripts
import fee_strategies
import placement_strategies

test_flag = 1
node_placement_amt = 5

if test_flag:
    print("testflag enabled!")
    data_path = 'data/testjson/'
    data_filename = 'testjson.json'
    tx_amts = [100, 10000, 1000000]
else:
    data_path = 'data/lnjson/'
    data_filename = 'ln.json'
    tx_amts = [100, 10000, 1000000]

g = nx.read_gml(data_path+"graph"+str(tx_amts[0])+".gml")
k2n = scripts.read_json(data_path+"key_to_node_map.json")
n2k = scripts.read_json(data_path+"node_to_key_map.json")
print("Base graph")
print(g.edges(data=True))
#print(k2n)
#print(n2k)

"""" There are 3 scenario's. 
    1. Where us and the network interact may optimize their solutions.
    2. Where us and the other party are allowed to optimize their solutions.
    3. Where us, the other, and the network are allowed to optimize their solutions. 
    
    For each of these scenarios all 6 placement strategies should be tested."""

# Add a party that represents "us" within the network
g, our_party_id = scripts.add_node(g)

# Add a party that represents the channels that will be created after us
g, other_party_id = scripts.add_node(g)

# Created the rewards table after all new parties have been created
rewards = scripts.init_reward_list(g)

# Allow the network to optimize their fees
# g = fee_strategies.graph_fee_optimization(g)

# Our party creates new channels
g = placement_strategies.uniform_random(g, our_party_id, node_placement_amt)
print("Added 'our' edges")
print(g.edges(data=True))

# Other party creates new channels
g = placement_strategies.uniform_random(g, other_party_id, node_placement_amt)
print("Added 'other' edges")
print(g.edges(data=True))

#rewards = scripts.calc_node_profit(g, rewards)
#g = fee_strategies.graph_fee_optimization(g)
#rewards = scripts.calc_node_profit(g, rewards)

#scripts.plot_rewards_graph(rewards, g.nodes())
