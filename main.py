import networkx as nx
import scripts

test_flag = 1

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
print(g.edges(data=True))
#print(k2n)
#print(n2k)

rewards = scripts.init_reward_list(g)

for i in range(4):
    rewards = scripts.calc_node_profit(g, rewards)

print(rewards)

scripts.plot_rewards_graph(rewards, g.nodes())
