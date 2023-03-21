import os
import json

input_file = "/data/yangyueting/Lateral/case_study/infer_output_GQ_s277_GPT-3-davinci-003_text.json"
can_file = "./candidates/text_GQ_can.txt"
ref_file = "./references/text_GQ_ref.txt"

with open(input_file,"r", encoding='utf-8') as fin, open(can_file,"a",encoding='utf-8') as fcan,  open(ref_file,"a",encoding='utf-8') as fref:
    dataset = json.load(fin)
    for item in dataset:
        # if "golden_question_list" in item and "golden_answer_list" in item:
        if "solution_history" in item:
            fref.write(item["final_answer"]+"\n")
            fcan.write(item["solution_history"][-1]+"\n")
fin.close()
fcan.close()
fref.close()
    