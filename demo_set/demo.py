from binhex import openrsrc
from curses import init_pair
import os
from unittest import result
import openai
import json
import argparse
import Levenshtein
from time import sleep
import sacrebleu
# from nltk.translate.bleu_score import sentence_bleu

openai.api_key = os.getenv("OPENAI_API_KEY")
example ={
        "puzzle": ["A man walks into a bar and asks the bartender for a drink of water.",
                    "The bartender pulls out a qun, points it at the man and cocks it. ",
                    "The man pauses before saying \"Thank you\"and leaving.",
                    "What happened?"
        ],
        "final_answer": ["The man had the hiccups."
                  "The bartender realized this and chose instead to cure the hiccups by frightening the man with the gun."
        ],
        "question_list":["Could the bartender hear him?",
                       "Did the man ask for water in an offensive way?"],
        "answer_list":["Yes.","No."],
        "hint":"As we said, there is nothing wrong with either the building or the elevator. There is, however, some feature of the man that causes him to take the stairs from the seventh floor."
    }

def waitforGPT(sec):
    sleep(sec)

def load_data(data_path):
    with open(data_path, 'r') as f:
        data_set = json.load(f)
    return data_set

def extract_input_item(data):
    puzzle = "".join(data["puzzle"])
    truth = "".join(data["final_answer"])
    fol_q = list(data["question_list"])
    fol_a = list(data["answer_list"])
    return puzzle, truth, fol_q, fol_a

def get_response(prompt):
    output_ai = ""
    response_num = 0
    while output_ai == "" and response_num <= 3:
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            temperature=0.7,
            max_tokens=100,
            top_p=1,
            logprobs = 5,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n\n"]
            )
        output_ai = response.get('choices')[0]['text'].split("\n")[0]
        log_info = response.get('choices')[0]
        if output_ai == "":
            response_num += 1
            waitforGPT(10)
    return output_ai,log_info

def question_generation_input(data_item):
    task_description = "I am an intelligent bot that can play situation puzzles with user. A puzzle is given first, and the user begin to ask a \"yes/no\" question to ensure details."
    # task_description = "question generation"
    puzzle, truth, fol_q, fol_a = extract_input_item(data_item)
    example_prefix = "puzzle:" + "".join(example["puzzle"]) + "\n"
    example_prefix += "follow_up_Q:"+example["question_list"][0]+"\n"+"follow_up_A:"+example["answer_list"][0] + "\n"
    example_prefix += "follow_up_Q:"+example["question_list"][1] + "\n"
    input_prefix = "puzzle:" + puzzle + "\n"  
    if len(fol_q) and len(fol_a):
        for fq,fa in zip(fol_q, fol_a):
            input_prefix += "follow_up_Q:"+ fq
            input_prefix += "follow_up_A:"+ fa
        input_prefix += "\n"
    input_prefix += "follow_up_Q:"
    final_prefix = task_description + '\n' + example_prefix + input_prefix
    # print("---------- question generation ----------")
    # print(final_prefix)
    return final_prefix

def answer_generation_input(data_item):
    task_description = "I am an intelligent bot that can play as judge in situation puzzles with user. A puzzle is given first, and the user begin to ask a \"yes/no\" question to ensure details, and I will give \"Yes/No/Irrelevent\" as answer to questions."
    # task_description = "answer generation"
    puzzle, truth, fol_q, fol_a = extract_input_item(data_item)
    example_prefix = "truth:" + "".join(example["final_answer"]) + "\n"
    example_prefix += "follow_up_Q:"+example["question_list"][0]+ "\n" +"follow_up_A:"+example["answer_list"][0] + "\n"
    example_prefix += "follow_up_Q:"+example["question_list"][1]+ "\n" +"follow_up_A:"+example["answer_list"][1] + "\n"
    input_prefix = "truth:" + truth + "\n"  
    if len(fol_q) and len(fol_a):
        for fq,fa in zip(fol_q, fol_a):
            input_prefix += "follow_ip_Q:"+ fq
            input_prefix += "follow_ip_A:"+ fa
    input_prefix += "follow_up_Q:" + data_item["question_list"][-1] 
    input_prefix += "\n" + "follow_up_A:"
    final_prefix = task_description + '\n' + example_prefix + input_prefix
    # print("---------- answer generation ----------")
    # print(final_prefix)
    return final_prefix
    
def solution_generate_input(data_item, shuffle):
    task_description = "I am an intelligent bot that can play situation puzzles with user. A puzzle is given first, and the user begin to ask \"yes/no\" question to ensure details, then I will give the question a\"yes/no/irrelevent\" answer. Finally user try to give solution for the puzzle."
    puzzle, truth, fol_q, fol_a = extract_input_item(data_item)
    if shuffle == "True":
        randomnum = random.randint(0,5)
        random.seed(randomnum)
        random.shuffle(fol_q)
        random.seed(randomnum)
        random.shuffle(fol_a)
    example_prefix = "puzzle:" + "".join(example["puzzle"]) + "\n"
    example_prefix += "follow_up_Q:"+example["question_list"][0]+"\n"+"follow_up_A:"+example["answer_list"][0] + "\n"
    example_prefix += "solution:" + "".join(example["final_answer"]) + "\n"
    input_prefix = "puzzle:" + puzzle + "\n"  
    if len(fol_q) and len(fol_a):
        for fq,fa in zip(fol_q, fol_a):
            input_prefix += "follow_up_Q:"+ fq +"\n"
            input_prefix += "follow_up_A:"+ fa+"\n"
        # input_prefix += "\n"
    input_prefix += "solution:"
    final_prefix = task_description + '\n' + example_prefix + input_prefix
    # print("---------- solution generation ----------")
    # print(final_prefix)
    return final_prefix

if __name__=="__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument('--dataset_path', type=str, default="../data/lateral_data.json")
    parse.add_argument('--sample_num', type=int, default=101)
    parse.add_argument('--chance_num', type=int, default=5)
    parse.add_argument('--threshold', type=int, default=0.65)
    # parse.add_argument('--output_log', type=str, default="./output/solution_log_output.json")
    parse.add_argument('--output_dataset', type=str, default="./output/final_data_output_100.json")
    # parse.add_argument('--with_hint', action='store_true')
    args = parse.parse_args()
    dataset = load_data(args.dataset_path)
    YNI =["Yes.", "No.", "Irrelevant."]
    for ditem in dataset[100:101]:
        print("PUZZLE:",ditem["puzzle"])
        chance_count = 0
        while chance_count < args.chance_num:
            # genrate question
            question_generation_prompt = question_generation_input(ditem)
            generated_question, _ = get_response(question_generation_prompt)
            ditem["question_list"].append(generated_question)
            # generate answer
            waitforGPT(10)
            answer_generation_prompt = answer_generation_input(ditem)
            generated_answer, _ = get_response(answer_generation_prompt)
            if generated_answer in YNI:
                ditem["answer_list"].append(generated_answer)
                print("*",generated_question)
                print("*",generated_answer)
            else:
                ditem["question_list"].pop()
                continue
            waitforGPT(10)
            # generate solution
            solution_generate_prompt = solution_generate_input(ditem,shuffle=False)
            # solution_generate_prompt = solution_generate_input(ditem)
            generated_solution, solution_log_info = get_response(solution_generate_prompt)               
            chance_count += 1
            if generated_solution == "":
                ditem["question_list"].pop()
                ditem["answer_list"].pop()
                continue
            print("*",generated_solution)
            if 'solution_list' not in ditem:
                ditem["solution_list"] = [generated_solution]
            else:
                ditem['solution_list'].append(generated_solution)
            if 'log_info' not in ditem:
                ditem['log_info'] = [solution_log_info]
            else:
                ditem['log_info'].append(solution_log_info)
            # calculate the current solution's accuracy：Jaro-Winkler
            similarity_score = Levenshtein.jaro_winkler("".join(ditem["final_answer"]),generated_solution)
            if 'edit_score' not in ditem:
                ditem["edit_score"] = [similarity_score]
            else:
                ditem["edit_score"].append(similarity_score)
            print("Edit score is : ", similarity_score)
            # thershold
            if similarity_score >= args.threshold:
                break
            if chance_count == 3:
                waitforGPT(60)
            else:
                waitforGPT(10)
        with open(args.output_dataset,"w",encoding="utf-8") as fd:
            json.dump(dataset[100],fd)
    # 修改dataset写入    
    # with open(args.output_dataset,"w",encoding="utf-8") as fd:
    #     json.dump(dataset[:51],fd)