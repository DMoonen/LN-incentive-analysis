import scripts

test_flag = 1
scenarios = [1, 2, 3, 4]

if test_flag:
    print("testflag enabled!")
    data_path = 'data/testjsonlarge/'
    tx_amts = [100, 10000, 1000000]
else:
    data_path = 'data/lnjson/'
    tx_amts = [100, 10000, 1000000]

for tx in tx_amts[:1]:
    print("    Visualizing tx:", tx)
    print('        Visualizing Scenario: 1')
    plot_path = data_path+'results/'+'rewards_highest_degree_%s_scenario_1.json' % tx
    reward_data = scripts.read_json(plot_path)
    scripts.plot_rewards_graph(plot_path.replace(".json", ".png"), reward_data, [list(reward_data.keys())[-1]])

    print('        Visualizing Scenario: 2')
    plot_path = data_path + 'results/' + 'rewards_highest_degree_%s_scenario_2.json' % tx
    reward_data = scripts.read_json(plot_path)
    scripts.plot_rewards_graph(plot_path.replace(".json", ".png"), reward_data, [list(reward_data.keys())[-1]])

    print('        Visualizing Scenario: 3')
    plot_path = data_path + 'results/' + 'rewards_highest_degree_%s_scenario_3.json' % tx
    reward_data = scripts.read_json(plot_path)
    scripts.plot_rewards_graph(plot_path.replace(".json", ".png"), reward_data,
                               [list(reward_data.keys())[-2], list(reward_data.keys())[-1]])

    print('        Visualizing Scenario: 4')
    plot_path = data_path + 'results/' + 'rewards_highest_degree_%s_scenario_4.json' % tx
    reward_data = scripts.read_json(plot_path)
    scripts.plot_rewards_graph(plot_path.replace(".json", ".png"), reward_data,
                               [list(reward_data.keys())[-2], list(reward_data.keys())[-1]])
