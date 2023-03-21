import json

def avg_QA_num(output_file):
    with open(output_file, 'r',encoding="utf-8") as f:
        data_set = json.load(f)
    f.close()
    total_num, avg_num = 0, 0
    for ditem in data_set:
        total_num += len(ditem["edit_score"])
    avg_num = total_num / len(data_set)
    return avg_num

if __name__ =='__main__':
    # GPT_GPT
    # output_file = "../demo_set/output/final_data_output_101-149.json"
    # avg_num = avg_QA_num(output_file)
    # print(avg_num)
    # KG_GPT
    output_file_kg = "../KG_with_GPT/output/KG_final_data_output_50_100.json"
    avg_num = avg_QA_num(output_file_kg)
    print(avg_num)
