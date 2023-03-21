import json
def load_data(data_path):
    with open(data_path, 'r') as f:
        data_set = json.load(f)
    return data_set

if __name__=="__main__":
    dataset_path = "./merge_data.json"
    dataset = load_data(dataset_path)
    puzzle_path = "./KG_dataset/puzzle_data.txt"
    truth_path = "./KG_dataset/truth_data.txt"
    # with open(puzzle_path,"a+",encoding="utf-8") as fp1, open(truth_path, "a+",encoding="utf-8") as fp2:
    #     for ditem in dataset:
    #         fp1.write(ditem["puzzle"]+"\n")
    #         fp2.write("".join(ditem["final_answer"])+"\n")
    # fp1.close()
    # fp2.close()
    for index, line in enumerate(open(puzzle_path, 'r'), 1):
        with open('./KG_dataset/puzzle/%d.txt' % index, 'w+') as tmp:
            tmp.write(line)
    for index, line in enumerate(open(truth_path, 'r'), 1):
        with open('./KG_dataset/truth/%d.txt' % index, 'w+') as tmp:
            tmp.write(line)
