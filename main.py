from networkx import *
import scripts

data_path = 'data/'
data_filename = 'testjson.json'

scripts.convert_json_to_graph(data_path, data_filename)
