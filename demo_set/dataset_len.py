import json
def load_data(data_path):
    with open(data_path, 'r') as f:
        data_set = json.load(f)
    return data_set

dataset_path = "../data/merge_data.json"
dataset = load_data(dataset_path)
print(len(dataset))
