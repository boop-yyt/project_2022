from curses import init_pair
import os
from unittest import result
import openai
import json
import argparse
# from similarity import compute_cosine_similarity

openai.api_key = os.getenv("OPENAI_API_KEY")
example = {
        "puzzle": ["A man walks into a bar and asks the bartender for a drink of water.",
                    "The bartender pulls out a qun, points it at the man and cocks it. ",
                    "The man pauses before saying \"Thank you\"and leaving.",
                    "What happened?"
        ],
        "truth": ["The man had the hiccups."
                  "The bartender realized this and chose instead to cure the hiccups by frightening the man with the gun."
        ],
        "follow-up-Q":["Could the bartender hear him?",
                       "Did the man ask for water in an offensive way?"],
        "follow-up-A":["Yes.","No."],
        "hint":"As we said, there is nothing wrong with either the building or the elevator. There is, however, some feature of the man that causes him to take the stairs from the seventh floor."
    }

def load_data(data_path):
	with open(data_path, 'r') as f:
		data_set = json.load(f)
	return data_set

def extract_input_item(data):
    puzzle = "".join(data["puzzle"])
    truth = "".join(data["truth"])
    fol_q = list(data["follow-up-Q"])
    fol_a = list(data["follow-up-A"])
    return puzzle, truth, fol_q, fol_a

def get_response(prompt):
	response = openai.Completion.create(
		model="text-davinci-002",
		prompt=prompt,
		temperature=0.7,
		max_tokens=100,
		top_p=1,
		frequency_penalty=0.0,
		presence_penalty=0.0,
		stop=["\n\n"]
		)
	return response.get('choices')[0]['text'].split("\n")[0]

'''def get_response(prompt):
    text = "okkkkkkkkkkkkkkkk"
    return text
'''

def question_generation_input(data_item):
    task_decription = ""
    puzzle, truth, fol_q, fol_a = extract_input_item(data_item)
    example_prefix = "puzzle:" + "".join(example["puzzle"]) + "\n"
    example_prefix += "follow_up_QA:"+example["follow-up-Q"][0]+example["follow-up-A"][0] + "\n"
    example_prefix += "follow_up_Q:"+example["follow-up-Q"][1] + "\n"
    input_prefix = "puzzle:" + puzzle + "\n"  
    input_prefix += "follow_up_QA:"
    for fq,fa in zip(fol_q, fol_a):
        input_prefix += fq + fa
    input_prefix += "\n"+"follow_up_Q:"
    final_prefix = task_decription + '\n' + example_prefix + input_prefix
    print("---------- question generation ----------\n")
    print(final_prefix)
    return final_prefix

def answer_generation_input(data_item):
    task_decription = ""
    puzzle, truth, fol_q, fol_a = extract_input_item(data_item)
    example_prefix = "truth:" + "".join(example["truth"]) + "\n"
    example_prefix += "follow_up_QA:"+example["follow-up-Q"][0]+example["follow-up-A"][0]+"\n"
    example_prefix += "follow_up_Q:"+example["follow-up-Q"][1] + "\n"
    example_prefix += "follow_up_A:"+example["follow-up-A"][1] + "\n"
    input_prefix = "truth:" + truth + "\n"  
    input_prefix += "follow_up_QA:"
    if fol_q and fol_a:
        for fq,fa in zip(fol_q, fol_a):
            input_prefix += fq + fa
        input_prefix += "\n"+"follow_up_Q:" + data_item["follow-up-Q"][-1] 
    input_prefix += "\n" + "follow_up_A:"
    final_prefix = task_decription + '\n' + example_prefix + input_prefix
    return final_prefix

def solution_generate_input(data_item):
    task_decription = ""
    puzzle, truth, fol_q, fol_a = extract_input_item(data_item)
    example_prefix = "puzzle:" + "".join(example["puzzle"]) + "\n"
    example_prefix += "follow_up_QA:"+example["follow-up-Q"][0]+example["follow-up-A"][0]+"\n"
    example_prefix += "solution:" + "".join(example["truth"]) + "\n"
    input_prefix = "puzzle:" + puzzle + "\n"  
    input_prefix += "follow_up_QA:"
    if fol_q and fol_a:
        for fq,fa in zip(fol_q, fol_a):
            input_prefix += fq + fa
    input_prefix += "\n" + "solution:"
    final_prefix = task_decription + '\n' + example_prefix + input_prefix
    return final_prefix

if __name__=="__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument('--sample_num', type=int, default=1, help="the sample number to be infer")
    parse.add_argument('--chance_num', type=int, default=2)
    parse.add_argument('--threshold', type=int, default=0.8)
    # parse.add_argument('--with_hint', action='store_true')
    args = parse.parse_args()
    dataset = load_data("./example.json")
    dataset = list(dataset.values())
    output_file = "./Latral/output.txt"
    # print(extract_input_item(dataset[0]))
    # print(question_generation_prompt(dataset[0]))
    # print(answer_generation_prompt(dataset[0]))
    # print(solution_generate_prompt(dataset[0]))
    for ditem in dataset[:args.sample_num]:
        # print(data_item)
        chance_count = 0
        while chance_count < args.chance_num:
            # genrate question
            question_generation_prompt = question_generation_input(ditem)
            generated_question = get_response(question_generation_prompt)
            ditem["follow-up-Q"].append(generated_question)
            print("*",generated_question)
            # generate answer
            # answer_generation_prompt = answer_generation_input(ditem)
            # generated_answer = get_response(answer_generation_prompt)
            # ditem["follow-up-A"].append(generated_answer)
            # # generate solution
            # solution_generate_prompt = solution_generate_input(ditem)
            # generated_solution = get_response(solution_generate_prompt)
            # print(f"the {chance_count+1} chance's answer:", generated_solution)
            chance_count += 1
            # calculate the current solution's accuracy
        #     similarity_score = compute_cosine_similarity("".join(data_item["truth"]), generated_solution)
        #     if similarity_score >= args.threshold:
        #         break
        # with open(output_file,"w",encoding="utf-8") as fp:
        #     fp.write(generated_solution)