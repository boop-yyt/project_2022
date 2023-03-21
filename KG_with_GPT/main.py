from Answer import question_generation_input, solution_generate_input, answer_generation_input, get_response, load_data, waitforGPT
from Questioner import parse_sents, match_KG
import argparse
from binhex import openrsrc
from curses import init_pair
import os
from unittest import result
import openai
import json
import Levenshtein
from time import sleep
import sacrebleu

if __name__=="__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument('--dataset_path', type=str, default="../data/lateral_data.json")
    parse.add_argument('--annotaion_path', type=str, default="../data/ann_data.json")
    parse.add_argument('--sample_num', type=int, default=55)
    parse.add_argument('--chance_num', type=int, default=5)
    parse.add_argument('--threshold', type=int, default=0.65)
    parse.add_argument('--output_file', type=str, default="./output/output.txt")
    parse.add_argument('--output_dataset', type=str, default="./output/KG_final_data_output_101_149.json")
    args = parse.parse_args()
    dataset = load_data(args.dataset_path)
    ann_data = load_data(args.annotaion_path)
    YNI =["Yes.", "No.", "Irrelevant."]
    for ditem, anitem in zip(dataset[101:150], ann_data[101:150]):
        print("PUZZLE:",ditem["puzzle"])
        truth_triples = anitem["truth"]
        puzzle_triples = anitem["puzzle"]
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
            if generated_answer not in YNI:
                ditem["question_list"].pop()
                continue
            print("*",generated_question)
            # KG questioner's answer back
            question_triples = parse_sents(generated_question)
            if 'question_triples_list' not in ditem:
                ditem["question_triples_list"] = [question_triples]
            else:
                ditem["question_triples_list"].append(question_triples)         
            answer_from_KG = match_KG(question_triples, truth_triples, puzzle_triples)
            print("*",answer_from_KG)
            ditem["answer_list"].append(answer_from_KG)
            # generate solution
            solution_generate_prompt = solution_generate_input(ditem,shuffle=False)
            # solution_generate_prompt = solution_generate_input(ditem)
            generated_solution, solution_log_info = get_response(solution_generate_prompt)
            print("*",generated_solution)
            if 'solution_list' not in ditem:
                ditem["solution_list"] = [generated_solution]
            else:
                ditem['solution_list'].append(generated_solution)
            if 'log_info' not in ditem:
                ditem['log_info'] = [solution_log_info]
            else:
                ditem['log_info'].append(solution_log_info)
            chance_count += 1
            # calculate the current solution's accuracy：Jaro-Winkler
            similarity_score = Levenshtein.jaro_winkler("".join(ditem["final_answer"]),generated_solution)
            if 'edit_score' not in ditem:
                ditem["edit_score"] = [similarity_score]
            else:
                ditem["edit_score"].append(similarity_score)
            print("Edit score is : ", similarity_score)            
            if similarity_score >= args.threshold:
                break
            if chance_count == 3:
                waitforGPT(60)
            else:
                waitforGPT(10)    
        with open(args.output_dataset,"w",encoding="utf-8") as fd:
            json.dump(dataset[101:150],fd)