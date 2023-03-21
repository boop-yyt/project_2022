import os
import json
def load_data(data_path):
    with open(data_path, 'r') as f:
        data_set = json.load(f)
    return data_set

def convert_to_chatgpt_prefix(item_dict):
    # print(item_dict)
    # task_description = "You are now a language model capable of lateral thinking. Now let's play a game together. The rule is to give you a simple description of the puzzle. According to the puzzle, and some history Question-Answer pairs, you need to generate a solution of puzzle."
    # Is there a wound on his body? Yes.
    # Is the wound caused by a sharp object? Yes.
    # Is this water related to the wound? Yes.
    limit_prompt = "(Your answer is not over 100 tokens "
    solution_limit = "and you can only give one possible solution)"
    # result_prefix = "Puzzle:"+item_dict['puzzle']+ "QA-pairs:"
    result_prefix = "Puzzle:"+item_dict['puzzle']
    # if "question_list" in item_dict and "answer_list" in item_dict:
        # if item_dict["question_list"] and item_dict["answer_list"]
    # for question, answer in zip(item_dict['question_list'], item_dict['answer_list']):
    #     result_prefix += question
    #     result_prefix += answer
    result_prefix += limit_prompt
    result_prefix += solution_limit
    result_prefix += "\n"
    return result_prefix

if __name__=="__main__":
    input_file = "../data/lateral_data.json"
    output_file = "./chat_woQA_puzzle.txt"
    output_golden = "./chat_woQA_golden_puzzle.txt"
    dataset = load_data(input_file)
    for ditem in dataset:
        if "question_list" in ditem and "answer_list" in ditem and ditem["question_list"]==[] and ditem["answer_list"]==[]:
            chat_input = convert_to_chatgpt_prefix(ditem)
            with open(output_file,"a+",encoding="utf-8") as f:
                f.write(chat_input)
            with open(output_golden,"a+",encoding="utf-8") as fg:
                fg.write(ditem["final_answer"]+"\n")
