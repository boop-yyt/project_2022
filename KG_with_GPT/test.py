import json

def load_data(data_path):
    with open(data_path, 'r') as f:
        data_set = json.load(f)
    return data_set

ann_data = load_data("../data/ann_data.json")
for anitem in ann_data:
        truth_triples = anitem["truth"]
        print(truth_triples,"\n")