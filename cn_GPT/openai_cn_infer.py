import os
from unittest import result
import openai
import json
import argparse

openai.api_key = os.getenv("OPENAI_API_KEY")
example_data = {
	"puzzle":"一个人去酒吧，点了一杯水，营业员突然举枪指着他，他说了一声谢谢，回头走了。发生了什么事？",
	"question_list":[
		"营业员听到客人点水了吗？",
		"那人是以一种不礼貌的方式点了一杯水吗？"
	],
	"answer_list": [
		"是",
		"否"
	],
	"final_answer": "这个男子在不停地打嗝，希望喝口水缓解一下。服务员得知情况后掏出枪对着他的脸，吓他一跳，男子打嗝因此好了，所以说了谢谢就走了。"
}


def load_data(data_path):
	with open(data_path, 'r') as f:
		data = json.load(f)
	return data

def convert_to_question_generation_prefix(item_dict):
	task_description = "我是一个智能机器人，可以和用户一起玩情境猜谜游戏。首先给出一个谜题，用户开始问“是/否”问题来获取线索。"
	result_prefix = task_description+'\n'+"Puzzle: "+example_data['puzzle']+'\n'
	result_prefix += "Question: "+example_data["question_list"][0]+'\n'
	# result_prefix += "Answer: "+example_data["answer_list"][0]+'\n'
	# result_prefix += "Question: "+example_data["question_list"][1]+'\n'
	result_prefix += '\n'
	result_prefix += "Puzzle:"+item_dict['puzzle']+"为什么会这样？'+\n'
	if  'gen_question_list' in item_dict and 'gen_answer_list' in item_dict:
		if len(item_dict['gen_question_list']) and len(item_dict['gen_answer_list']):
			for fq,fa in zip(item_dict['gen_question_list'], item_dict['gen_answer_list']):
				result_prefix += "Question:"+ fq
				result_prefix += "Answer:"+ fa
	result_prefix += "Question: "
	return result_prefix


def convert_to_answer_generation_prefix(item_dict):
	task_description = "我是一个智能机器人，可以在与用户的情境猜谜游戏中充当判断者。首先给出一个谜题，用户开始问一个“是/否”的问题来获取线索，我将给出“是/否/与此无关”作为问题的答案。"
	result_prefix = task_description+'\n'+"Puzzle: "+example_data['puzzle']+'\n'
	result_prefix += "Solution: "+example_data["final_answer"]
	result_prefix += "Question: "+example_data["question_list"][0]+'\n'
	result_prefix += "Answer: "+example_data["answer_list"][0]+'\n'
	result_prefix += "Question: "+example_data["question_list"][1]+'\n'
	result_prefix += "Answer: "+example_data["answer_list"][1]+'\n'
	result_prefix += '\n'
	result_prefix += "Puzzle:"+item_dict['puzzle']+"为什么会这样？'+\n'
	result_prefix = "Solution:" + item_dict['final_answer'] + "\n" 
	if  'gen_question_list' in item_dict and 'gen_answer_list' in item_dict:
		if len(item_dict['gen_question_list']) and len(item_dict['gen_answer_list']):
			for fq,fa in zip(item_dict['gen_question_list'], item_dict['gen_answer_list']):
				result_prefix += "Question:"+ fq
				result_prefix += "Answer:"+ fa
	result_prefix += "Question:" + item_dict["gen_question_list"][-1] 
	result_prefix += "Answer: "
	return result_prefix

def convert_to_hint_generation_prefix(item_dict):
	pass

def convert_to_solution_generation_prefix(item_dict):
	task_description = "我是一个智能机器人，可以和用户一起玩情境猜谜游戏。首先给出一个谜题，用户开始问“是/否”问题以确保细节，然后我会给这个问题一个“是/否/与此无关”的答案。最后，我将尝试给出谜题的解决方案。"
	result_prefix = task_description+'\n'+"Puzzle: "+example_data['puzzle']+'\n'
	result_prefix += "Question: "+example_data["question_list"][0]+'\n'
	result_prefix += "Answer: "+example_data["answer_list"][0]+'\n'
	result_prefix += "Question: "+example_data["question_list"][1]+'\n'
	result_prefix += "Answer: "+example_data["answer_list"][1]+'\n'
	result_prefix += '\n'
	result_prefix += "Puzzle:"+item_dict['puzzle']+"为什么会这样？'+\n'
	if "gen_question_list" in item_dict and "gen_answer_list" in item_dict:
		for question, answer in zip(item_dict['gen_question_list'], item_dict['gen_answer_list']):
			result_prefix += "Question: "+question+'\n'
			result_prefix += "Answer: "+answer+'\n'
	result_prefix += "Solution: "
	return result_prefix

def Jaccard_similarity(infer_sent, ref):
	infer_sent_list = infer_sent.split(' ')
	ref_list = ref.split(' ')
	infer_sent_set = set(infer_sent_list)
	ref_set = set(ref_list)
	union_set = infer_sent_set.union(ref_set)
	intersetion_set = infer_sent_set.intersection(ref_set)
	jaccard_score = float(len(intersetion_set)/len(union_set))
	return jaccard_score


def get_response(prompt):
	response = openai.Completion.create(
		model="text-davinci-003",
		prompt=prompt,
		temperature=0.7,
		max_tokens=100,
		top_p=1,
		frequency_penalty=0.0,
		presence_penalty=0.0,
		stop=["\n\n"]
		)
	return response.get('choices')[0]['text'].split("\n")[0]

if __name__=="__main__":
	parse = argparse.ArgumentParser()
	parse.add_argument('--sample_num', type=int, default=1, help="the sample number to be infer")
	parse.add_argument('--max_turn', type=int, default=1)
	parse.add_argument('--with_hint', action='store_true')
	args = parse.parse_args()

	dataset = load_data("../data/cn_data.json")
	dataset = list(dataset.values())
	valid_answer =["是。","否。","与此无关。","是","否","与此无关"]
	for item in dataset[:args.sample_num]:
		print("PUZZLE:", item['puzzle'])
		turn_count = 0
		while turn_count < args.max_turn:
			question_generation_prompt = convert_to_question_generation_prefix(item)
			generated_question = get_response(question_generation_prompt)
			if 'gen_question_list' not in item:
				item["gen_question_list"] = [generated_question]
			else:
				item['gen_question_list'].append(generated_question)
			answer_generation_prompt = convert_to_answer_generation_prefix(item)
			generated_answer = get_response(answer_generation_prompt)
			if generated_answer in valid_answer:
				print("Q:",generated_question)
				print("A:",generated_answer)
				if 'gen_answer_list' not in item:
					item["gen_answer_list"] = [generated_answer]
				else:
					item["gen_answer_list"].append(generated_answer)
			else:
				item['gen_question_list'].pop(-1)
				continue
			# solution_generation_prompt = convert_to_solution_generation_prefix(item)
			# generated_solution = get_response(solution_generation_prompt)
			# print(f"turn_{turn_count+1}: ", generated_solution)
			# if 'solution_history' not in item:
			# 	item["solution_history"] = [generated_solution]
			# else:
			# 	item["solution_history"].append(generated_solution)
			# jaccard_score = Jaccard_similarity(generated_solution, item['answer'][0])
			# if jaccard_score>0.5:
			# 	break
			turn_count += 1
	# with open('output/infer_output.json', 'w') as f:
	# 	json.dump(dataset[:args.sample_num], f)