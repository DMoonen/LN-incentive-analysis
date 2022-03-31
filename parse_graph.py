import scripts

test_flag = 0

if test_flag:
    print("testflag enabled!")
    data_path = 'data/testjson/'
    data_filename = 'testjson.json'
    tx_amts = [100, 10000, 1000000]
else:
    data_path = 'data/lnjson/'
    data_filename = 'new.json'
    tx_amts = [100, 10000, 1000000]

scripts.convert_json_to_graph(data_path, data_filename, tx_amts)

