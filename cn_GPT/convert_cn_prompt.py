from collections import defaultdict
from typing import DefaultDict


example_data = {
	"puzzle":"一个人去酒吧，点了一杯水，营业员突然举枪指着他，他说了一声谢谢，回头走了。发生了什么事？",
	"question_list":[
		"营业员听到客人点水了吗？",
		"那人是以一种不礼貌的方式点了一杯水吗？"
	],
	"answer_list": [
		"是",
		"否"
	]
}

def convert_to_question_generation_prefix(item_dict):
	task_description = "我是一个智能机器人，可以和用户一起玩情境猜谜游戏。首先给出一个谜题，用户开始问“是/否”问题来获取线索。"

	result_prefix = task_description+'\n\n'+"Puzzle: "+example_data['puzzle']+'\n'
	result_prefix += "Question: "+example_data["question_list"][0]+'\n'
	result_prefix += "Answer: "+example_data["answer_list"][0]+'\n'
	result_prefix += "Question: "+example_data["question_list"][1]+'\n'
	result_prefix += '\n'
	result_prefix += "Puzzle:"+item_dict['puzzle']+'\n'
	if "gen_question_list" in item_dict:
		for question, answer in zip(item_dict['gen_question_list'], item_dict['gen_answer_list']):
			result_prefix += "Question: "+question+'\n'
			result_prefix += "Answer: "+answer+'\n'


	result_prefix += "Question: "
	return result_prefix


def convert_to_answer_generation_prefix(item_dict):
	task_description = "我是一个智能机器人，可以在与用户的情境猜谜游戏中充当判断者。首先给出一个谜题，用户开始问一个“是/否”的问题来获取线索，我将给出“是/否/与此无关”作为问题的答案。"
	result_prefix = task_description+'\n\n'+"Puzzle: "+example_data['puzzle']+'\n'
	result_prefix += "Solution: "+example_data["final_answer"]
	result_prefix += "Question: "+example_data["question_list"][0]+'\n'
	result_prefix += "Answer: "+example_data["answer_list"][0]+'\n'
	result_prefix += "Question: "+example_data["question_list"][1]+'\n'
	result_prefix += "Answer: "+example_data["answer_list"][1]+'\n'
	result_prefix += '\n'
	result_prefix += "Puzzle:"+item_dict['puzzle']+'\n'
	if "gen_question_list" in item_dict and "gen_answer_list" in item_dict:
		for question, answer in zip(item_dict['gen_question_list'], item_dict['gen_answer_list']):
			result_prefix += "Question: "+question+'\n'
			result_prefix += "Answer: "+answer+'\n'

	result_prefix += "Question: "+item_dict['gen_question_list'][-1]+'\n'
	result_prefix += "Answer: "
	return result_prefix


def convert_to_answer_prefix(item_dict, question_list, answer_list):
	task_description = "I am an intelligent bot that can play as judge in situation puzzles with user. A puzzle is given first, and the user begin to ask a \"yes/no\" question to ensure details, and I will give \"Yes/No/Irrelevent\" as answer to questions."
	# task_description = "I can answer the question with only yes or no or irrelevant with the \"truth\". "
	result_prefix = task_description+'\n\n'+"Puzzle: "+example_data['puzzle']+'\n'
	result_prefix += "Solution: "+example_data["final_answer"]
	result_prefix += "Question: "+example_data["question_list"][0]+'\n'
	result_prefix += "Answer: "+example_data["answer_list"][0]+'\n'
	result_prefix += "Question: "+example_data["question_list"][1]+'\n'
	result_prefix += "Answer: "+example_data["answer_list"][1]+'\n'
	result_prefix += '\n'
	result_prefix += "Puzzle:"+item_dict['puzzle']+'\n'
	
	for question, answer in zip(question_list, answer_list):
		result_prefix += "Question: "+question+'\n'
		result_prefix += "Answer: "+answer+'\n'

	result_prefix += "Question: "+question_list[-1]+'\n'
	result_prefix += "Answer: "
	return result_prefix

def convert_to_solution_generation_prefix(item_dict, with_hint, golden_history=False):
	task_description = "我是一个智能机器人，可以和用户一起玩情境猜谜游戏。首先给出一个谜题，用户开始问“是/否”问题以确保细节，然后我会给这个问题一个“是/否/与此无关”的答案。最后，我将尝试给出谜题的解决方案。"
	reject_hint = "You should ask \"yes/no\" question only."
	hint_dict = {}
	hint_dict['Yes'] = ', correctly think!'
	hint_dict['Yes.'] = ' Correctly think!'
	hint_dict['No'] = ', reverse thinking!'
	hint_dict['No.'] = ' Reverse thinking!'
	hint_dict['Irrelevant'] = ', think differently!'
	hint_dict['Irrelevant.'] = ' Think differently!'

	result_prefix = task_description+'\n\n'+"Puzzle: "+example_data['puzzle']+'\n'
	result_prefix += "Question: "+example_data["question_list"][0]+'\n'
	result_prefix += "Answer: "+example_data["answer_list"][0]+'\n'
	result_prefix += "Question: "+example_data["question_list"][1]+'\n'
	result_prefix += "Answer: "+example_data["answer_list"][1]+'\n'
	result_prefix += '\n'
	result_prefix += "Puzzle:"+item_dict['puzzle']+'\n'
	if "gen_question_list" in item_dict and "gen_answer_list" in item_dict and not golden_history:
		for question, answer in zip(item_dict['gen_question_list'], item_dict['gen_answer_list']):
			if with_hint:
				if answer in hint_dict:
					result_prefix += "Question: "+question+'\n'
					result_prefix += "Answer: "+answer+hint_dict[answer]+'\n'
				else:
					result_prefix +=f"Tips: {reject_hint}\n"
				
			else:
				if answer in hint_dict:
					result_prefix += "Question: "+question+'\n'
					result_prefix += "Answer: "+answer+'\n'
	else:
		for question, answer in zip(item_dict['question_list'], item_dict['answer_list']):
			if with_hint:
				if answer in hint_dict:
					result_prefix += "Question: "+question+'\n'
					result_prefix += "Answer: "+answer+hint_dict[answer]+'\n'
				else:
					result_prefix +=f"Tips: {reject_hint}\n"
				
			else:
				if answer in hint_dict:
					result_prefix += "Question: "+question+'\n'
					result_prefix += "Answer: "+answer+'\n'
	result_prefix += f"Solution: "
	return result_prefix