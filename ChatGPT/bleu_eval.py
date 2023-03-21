import os
os.environ["NUM_WORKERS"] = "1"
os.environ['CUDA_VISIBLE_DEVICES'] = '7'
from typing import DefaultDict
from lmqg.automatic_evaluation_tool.bleu.bleu import Bleu
from lmqg.automatic_evaluation_tool.rouge import Rouge
from lmqg.automatic_evaluation_tool.bertscore import BERTScore
from lmqg.automatic_evaluation_tool.moverscore import MoverScore
import argparse
import json
import csv
# from bleurt import score
import numpy as np
from chat_prompt import load_data

parser = argparse.ArgumentParser()
# parser.add_argument('--eval_file_path', type=str, default="./chat_limit_output/output_limit.txt")
# parser.add_argument('--golden_file_path', type=str, default="/data/yangyueting/Lateral/case_study/references/chatgpt_ref.txt")
# parser.add_argument('--eval_file_path', type=str, default="../case_study/infer_output_s277_GPT-3-davinci-003_text.json")
# parser.add_argument('--golden_file_path', type=str, default="../data/lateral_data.json")
# parser.add_argument('--eval_file_path', type=str, default="../case_study/infer_output_s277_GPT-3-davinci-003_kg.json")
# parser.add_argument('--golden_file_path', type=str, default="../data/lateral_data.json")
# parser.add_argument('--eval_file_path', type=str, default="/data/yangyueting/Lateral/ChatGPT/html-output/output_open.txt")
# parser.add_argument('--golden_file_path', type=str, default="/data/yangyueting/Lateral/ChatGPT/input-data/chat_golden_open.txt")
# parser.add_argument('--eval_file_path', type=str, default="/data/yangyueting/Lateral/case_study/candidates/text_can.txt")
# parser.add_argument('--golden_file_path', type=str, default="/data/yangyueting/Lateral/case_study/references/text_ref.txt")
# limit_text_path = "/data/yangyueting/Lateral/case_study/candidates/text_GQ_can.txt"
# golden_text_path ="/data/yangyueting/Lateral/case_study/references/text_GQ_ref.txt"
parser.add_argument('--eval_file_path', type=str, default="/data/yangyueting/Lateral/case_study/candidates/text_GQ_can.txt")
parser.add_argument('--golden_file_path', type=str, default="/data/yangyueting/Lateral/case_study/references/text_GQ_ref.txt")

args = parser.parse_args()
#chatgpt
with open(args.eval_file_path, "r", encoding="utf-8") as f:
    generate_solution = f.readlines()
with open(args.golden_file_path, "r", encoding="utf-8") as f:
    golden_solution = f.readlines()
# json
# generate_dataset = load_data(args.eval_file_path)
# generate_solution = []
# for item in generate_dataset:
#         generate_solution.append(item["solution_history"][-1])

# golden_dataset = load_data(args.golden_file_path)
# golden_solution = []
# for item in golden_dataset:
#         golden_solution.append(item["final_answer"])

solution_ref = DefaultDict()
solution_hypo = DefaultDict()

for t_item,s_item in zip(golden_solution,generate_solution):
    try:
        solution_ref[f"solution_{len(solution_ref)}"] = [t_item.encode()]
    except:
        solution_ref[f"solution_{len(solution_ref)}"] = [t_item.encode()]
    solution_hypo[f"solution_{len(solution_hypo)}"] = [s_item.encode()]

# import ipdb;ipdb.set_trace()
output_csv_name = "./puzzle__total_bleu_metric.csv"
f = open(output_csv_name, 'w')
csv_writer = csv.writer(f, delimiter=',')
csv_writer.writerow(["metric", "solution_score"])
for scorer, method in [(Bleu(4), ["Bleu-1", "Bleu-2", "Bleu-3", "Bleu-4"])]:
    puzzle_score, puzzle_scores = scorer.compute_score(solution_ref, solution_hypo)
    # puzzle_score = scorer.compute_score(solution_ref, solution_hypo)
    if isinstance(puzzle_scores, list):
        for m, ps in zip(method, puzzle_score):
            csv_writer.writerow([m, ps])
    else:
        csv_writer.writerow([method, puzzle_scores])    
    print(f"{method}  puzzle:{puzzle_score}")

# import ipdb;ipdb.set_trace()
# output_csv_name = args.eval_file_path.replace('.json', '_metric.csv')
# f = open(output_csv_name, 'w')
# csv_writer = csv.writer(f, delimiter=',')
# csv_writer.writerow(["metric", "solution_score"])
# for scorer, method in [(Bleu(4), ["Bleu-1", "Bleu-2", "Bleu-3", "Bleu-4"])]:
#     puzzle_score, puzzle_scores = scorer.compute_score(golden_solution, generate_solution)
#     if isinstance(puzzle_score, list):
#         for m, ps in zip(method, puzzle_score):
#             csv_writer.writerow([m, ps])
#     else:
#         csv_writer.writerow([method, puzzle_score])
#     print(f"{method}  puzzle:{puzzle_score}")

# scorer = score.BleurtScorer()
# bleurt_solution_score = scorer.score(
#     references=[sent for sent in golden_solution], 
#     candidates=[sent for sent in generate_solution]
#     )

# csv_writer.writerow(['BLEURT', np.mean(bleurt_solution_score)])
