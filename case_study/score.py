from bleurt import score
# from bert_score import score
import json
import csv
import os
import numpy as np
import Levenshtein
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

os.environ['CUDA_VISIBLE_DEVICES'] = '6'

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

checkpoint = "../../bleurt/BLEURT-20"
scorer = score.BleurtScorer(checkpoint)

text_output_path = "./infer_output_s277_GPT-3-davinci-003_text.json"
kg_output_path = "./infer_output_s277_GPT-3-davinci-003_kg.json"
goldenQA_output_path = "./GQA_davinci-003_full-dataset.json"
output_csv_name = './kg_GQ_metric.csv'
f = open(output_csv_name, 'w')
csv_writer = csv.writer(f, delimiter=',')
# limit_text_path = "/data/yangyueting/Lateral/ChatGPT/html-output/output_open.txt"
open_text_path = "../ChatGPT/chat_html/chat_output.txt"
# golden_text_path ="/data/yangyueting/Lateral/ChatGPT/input-data/chat_golden_open.txt"
limit_text_path = "/data/yangyueting/Lateral/case_study/candidates/kg_GQ_can.txt"
golden_text_path ="/data/yangyueting/Lateral/case_study/references/kg_GQ_ref.txt"

# golden QA bleurt
# with open(goldenQA_output_path,"r",encoding="utf-8") as f_g:
#     GQA_dataset = json.load(f_g)

# bleurt_GQA_score = scorer.score(
#     references=[sent["final_answer"] for sent in GQA_dataset], 
#     candidates=[sent["solution_history"][-1] for sent in GQA_dataset]
#     )
# csv_writer.writerow(['BLEURT', 'bleurt_GQA_score'])
# for score  in bleurt_GQA_score:
#     csv_writer.writerow(['', score])
# csv_writer.writerow(['final',np.mean(bleurt_GQA_score)])   
# chatgpt bleurt
# with open(golden_text_path,"r", encoding='utf-8') as f:
#     golden_dataset = json.load(f)
# golden_solution = []
# for item in golden_dataset:
#     if "golden_question_list" in item and "golden_answer_list" in item:
#         golden_solution.append(item["final_answer"])

with open(limit_text_path) as f_limit, open(golden_text_path) as f_golden:
    limit_can = [line.strip() for line in f_limit]
    golden_solution = [line.strip() for line in f_golden]

bleurt_limit_score = scorer.score(
    references=[sent for sent in golden_solution], 
    candidates=[sent for sent in limit_can]
    )
csv_writer.writerow(['BLEURT', 'bleurt_open_score'])
for t_score in bleurt_limit_score:
    csv_writer.writerow(['', t_score])
csv_writer.writerow(['final',np.mean(bleurt_limit_score)])
# bleurt_open_score = scorer.score(
#     references=[sent for sent in golden_solution],
#     candidates=[sent for sent in open_can]
#     )

# csv_writer.writerow(['BLEURT', 'bleurt_limit_score', 'bleurt_open_score'])
# for t_score, kg_score in zip(bleurt_limit_score, bleurt_open_score):
#     csv_writer.writerow(['', t_score, kg_score])
# csv_writer.writerow(['final',np.mean(bleurt_limit_score), np.mean(bleurt_open_score)])

# text-kg bleurt
# with open(text_output_path,"r",encoding="utf-8") as f_text, open(kg_output_path,"r",encoding="utf-8") as f_kg:
#     text_dataset = json.load(f_text)
#     kg_dataset = json.load(f_kg)

# bleurt_text_score = scorer.score(
#     references=[sent["final_answer"] for sent in text_dataset], 
#     candidates=[sent["solution_history"][-1] for sent in text_dataset]
#     )

# bleurt_kg_score = scorer.score(
#     references=[sent["final_answer"] for sent in kg_dataset], 
#     candidates=[sent["solution_history"][-1] for sent in kg_dataset]
#     )

# csv_writer.writerow(['BLEURT', 'bleurt_text_score', 'bleurt_kg_score'])
# text_count, kg_count = 0, 0
# for t_score, kg_score in zip(bleurt_text_score, bleurt_kg_score):
#     csv_writer.writerow(['', t_score, kg_score])
# csv_writer.writerow(['final',np.mean(bleurt_text_score), np.mean(bleurt_kg_score)])

# sem score
# with open(golden_text_path,"r", encoding='utf-8') as f:
#     golden_dataset = json.load(f)
# golden_solution = []
# for item in golden_dataset:
#     if "golden_question_list" in item and "golden_answer_list" in item:
#         golden_solution.append(item["final_answer"])

# with open(limit_text_path) as f_limit, open(open_text_path) as f_open:
#     limit_refs = [line.strip() for line in f_limit]
#     open_refs = [line.strip() for line in f_open]

# golden_vector = [model.encode(solution.split('\t'),convert_to_tensor=True).cpu() for solution in golden_solution]
# limit_vector  = [model.encode(limit.split('\t'), convert_to_tensor=True).cpu() for limit in limit_refs]
# open_vector  = [model.encode(open_text.split('\t'), convert_to_tensor=True).cpu() for open_text in open_refs]

# score_sem_limit = [cosine_similarity(vector1,vector2) for vector1,vector2 in zip(golden_vector, limit_vector)]
# score_sem_open = [cosine_similarity(vector1,vector2) for vector1,vector2 in zip(golden_vector, open_vector)]

# golden_cands = [solution for solution in golden_solution]
# Pt,Rt,score_bert_limit = score(golden_cands, limit_refs, lang='en', verbose=True)
# Pkg,Rkg,score_bert_open = score(golden_cands, open_refs, lang='en', verbose=True)

# csv_writer.writerow(['', 'cos-sem-score','bert-score'])
# csv_writer.writerow(['limit_score', np.mean(score_sem_limit), score_bert_limit.mean()])
# csv_writer.writerow(['open_score', np.mean(score_sem_open), score_bert_open.mean()])

# truth_vector = [model.encode(solution["final_answer"].split('\t'),convert_to_tensor=True).cpu() for solution in text_dataset]
# text_vector  = [model.encode(solution["solution_history"][-1].split('\t'), convert_to_tensor=True).cpu() for solution in text_dataset]
# kg_vector  = [model.encode(solution["solution_history"][-1].split('\t'), convert_to_tensor=True).cpu() for solution in kg_dataset]

# score_sem_golden = [cosine_similarity(vector1,vector2) for vector1,vector2 in zip(truth_vector, truth_vector)]
# score_sem_text = [cosine_similarity(vector1,vector2) for vector1,vector2 in zip(truth_vector, text_vector)]
# score_sem_kg = [cosine_similarity(vector1,vector2) for vector1,vector2 in zip(truth_vector, kg_vector)]


# golden_cands = [solution['final_answer'] for solution in text_dataset]
# text_refs = [solution["solution_history"][-1] for solution in text_dataset]
# kg_refs = [solution["solution_history"][-1] for solution in kg_dataset]
# Pt,Rt,score_bert_text = score(golden_cands, text_refs, lang='en', verbose=True)
# Pkg,Rkg,score_bert_kg = score(golden_cands, kg_refs, lang='en', verbose=True)

# csv_writer.writerow(['Bert-score', 'text_score', 'kg_score'])
# for t_score, kg_score in zip(score_bert_text, score_bert_kg):
#     csv_writer.writerow(['', t_score, kg_score])

# csv_writer.writerow(['total_count', text_count, kg_count])

# csv_writer.writerow(['', 'cos-sem-score','bert-score'])
# csv_writer.writerow(['text_score', np.mean(score_sem_text), score_bert_text.mean()])
# csv_writer.writerow(['kg_score', np.mean(score_sem_kg), score_bert_kg.mean()])

# csv_writer.writerow(['','cos_similarity'])
# csv_writer.writerow(['golden_score', np.mean(score_sem_golden)])
# csv_writer.writerow(['text_score', np.mean(score_sem_text)])
# csv_writer.writerow(['kg_score', np.mean(score_sem_kg)])

# csv_writer.writerow(['', 'bert-score'])
# csv_writer.writerow(['text_score', score_bert_text.mean()])
# csv_writer.writerow(['kg_score', score_bert_kg.mean()])



# embedding_1= model.encode(list1, convert_to_tensor=True)
# embedding_2 = model.encode(list2, convert_to_tensor=True)
# cosine_similarity(embedding_1.cpu(), embedding_2.cpu())
