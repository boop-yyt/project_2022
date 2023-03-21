from difflib import SequenceMatcher
import amrlib
import json
from SentParse import convert_sent2EventGraph

# "Event":[["back", "ball", "physics professor"]]
# generated_question = "Is this relate to the ball"
# question_triples = {"Entity":[],"Event":[],"Relation":[]}
# truth_triples = { "Event":[   ['demonstrating', 'physics professor', None], 
#                     ['suspending', 'physics professor', None], 
#                     ['pulls', 'physics professor', None], 
#                     ['back', 'ball', None], 
#                     ['right in front of', 'ball', None], 
#                     ['lets go', 'ball', None], 
#                     ['supposed', 'physics professor', None], 
#                     ['swing away from', 'physics professor', None],
#                     ['back', 'ball', 'physics professor'], 
#                     ['stopping', 'ball', 'physics professor'], 
#                     ['in front of', 'his nose', None], 
#                     ['gave', 'physics professor', None], 
#                     ['a slight push', 'ball', None], 
#                     ['crashing into', 'ball', 'his nose']],
#                     "Entity":["ball","physics professor"]
#                 }

def match_KG(question_triples, truth_triples, puzzle_triples):
    answer_back = ""
    if question_triples.get("Event") == [] and question_triples.get("Relation") == []:
        if question_triples.get("Entity") == []:
            return "No."
        else:
            for q in question_triples["Entity"]:
                if q in truth_triples["Entity"]:
                    answer_back = "Yes."
                else:
                    answer_back = "No."
    else:
        for q_event in question_triples["Event"]:
            for event in truth_triples["Event"]:
                if event[0] == q_event[0]:
                    if SequenceMatcher(None, event[1:3], q_event[1:3]).ratio() == 1.0:
                        answer_back = "Yes."
                        break
                    else:
                        answer_back = "No."
                        continue
                else:
                    answer_back = "Irrelevant."
                    continue
    if question_triples.get("Event") == [] and question_triples.get("Relation") == []:
        if question_triples.get("Entity") == []:
            return "No."
        else:
            for q in question_triples["Entity"]:
                if q in puzzle_triples["Entity"]:
                    answer_back = "Yes."
                else:
                    answer_back = "No."
    else:
        for q_event in question_triples["Event"]:
            for event in puzzle_triples["Event"]:
                if event[0] == q_event[0]:
                    if SequenceMatcher(None, event[1:3], q_event[1:3]).ratio() == 1.0:
                        answer_back = "Yes."
                        break
                    else:
                        answer_back = "No."
                        continue
                else:
                    answer_back = "Irrelevant."
                    continue
    return answer_back


def parse_sents(generated_question):
    span_dict, relation_dict, event_dict = convert_sent2EventGraph(generated_question)
    # print("span_dict:", span_dict)
    # print("relation_dict", relation_dict)
    # print("event_dict:", event_dict)
    # span_dict = {'T1': ['Event', '13', '16', 'hit'], 'T2': ['Head_End', '8', '12', 'ball'], 'T3': ['Head_End', '21', '24', 'man']}
    # relation_dict = {}
    # event_dict = {'E1': ['Event:T1', 'Head:T2', 'End:T3']}
    question_tri_path = "./question_ann.json"
    entity_set, relation_set, event_set = [],[],[]
    for span in span_dict.values():
        if span[0] == "Head_End":
            entity_set.append(span[3])
    for event in event_dict.values():
        # print(span_dict.get(event[0][event[0].rfind(":")+1:])[3],"\n",
        #                     span_dict.get(event[1][event[1].rfind(":")+1:])[3], "\n",
        #                     span_dict.get(event[2][event[2].rfind(":")+1:])[3])
        if len(event) == 2:
            event_set.append([  span_dict.get(event[0][event[0].rfind(":")+1:])[3],
                                span_dict.get(event[1][event[1].rfind(":")+1:])[3]])
        if len(event) == 3:
            event_set.append([  span_dict.get(event[0][event[0].rfind(":")+1:])[3],
                                span_dict.get(event[1][event[1].rfind(":")+1:])[3], 
                                span_dict.get(event[2][event[2].rfind(":")+1:])[3]])
    question_triples = {"Entity":entity_set,"Relation":relation_set, "Event":event_set} 
    with open(question_tri_path, "a+", encoding="utf-8") as fd:
        json.dump(question_triples, fd)
        fd.close()
    return question_triples

# print("answer_back:",match_KG(question_triples, truth_triples))
# generated_question = "Did the man die of thirst?"
# print(parse_sents(generated_question))
# parse_sents(generated_question)
# print(parse_sents())
# print(match_KG(question_triples, truth_triples))