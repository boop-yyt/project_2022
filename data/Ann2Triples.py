import codecs
import os
import difflib
import random
import Levenshtein
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import gensim
import json


def Ann2Triples(annfile):
  puzzle_entity_dict, Event_dict = {}, {}
  Entity_set, Event_set = [], []
  relation_list = []
  Event_list = []
  # with open(annfile,"r", encoding="utf-8") as f:
  for line in annfile.readlines():
        a = line.split()
        # print(a)
        if a[0][0]=="T" :
          if a[1] == "Head_End":
            Entity_set.append(" ".join(a[4:]))
          if a[1] == "Event":
            Event_set.append(" ".join(a[4:]))
          puzzle_entity_dict[a[0]] = " ".join(a[4:])
        if a[0][0] == "E":
          event_triples = []
          if a[1][:a[1].rfind(":")] == "Non_Core_Event":
            if len(a) > 2:
              event, head = a[1][a[1].rfind(":")+1:], a[2][a[2].rfind(":")+1:]
              event_triples.extend([event, head, None])
            else:
              event = a[1][a[1].rfind(":")+1:]
              event_triples.extend([event, None, None])
            # print("event_triples:", event_triples)
          if a[1][:a[1].rfind(":")] == "Event":
            event = a[1][a[1].rfind(":")+1:]
            if len(a) > 2:
              head = a[2][a[2].rfind(":")+1:]
            else:
              head = None
            if len(a) > 3:
              end = a[3][a[3].rfind(":")+1:]
            else:
              end = None
            event_triples.extend([event, head, end])
          Event_dict[a[0]] = event_triples
          event_temp = []
          if event_triples[2] == None:
            event_temp.extend([puzzle_entity_dict.get(event_triples[0]), puzzle_entity_dict.get(event_triples[1]), None])
          else:
            event_temp.extend([puzzle_entity_dict.get(event_triples[0]), puzzle_entity_dict.get(event_triples[1]), puzzle_entity_dict.get(event_triples[2])])   
          Event_list.append(event_temp)
        if a[0][0]=="R":
          relation_triples = []
          Arg1 = a[2][a[2].rfind(":")+1:]
          Arg2 = a[3][a[3].rfind(":")+1:]
          while Arg1[0] == "E":
            Arg1 = Event_dict.get(Arg1)[0]
          while Arg2[0] == "E":
            Arg2 = Event_dict.get(Arg2)[0]
          relation_triples.extend([a[1], puzzle_entity_dict.get(Arg1), puzzle_entity_dict.get(Arg2)])
          relation_list.append(relation_triples)
  return Entity_set, relation_list, Event_list

def puzzle_truth_ann():
  ann_data_path = "./ann_data.json"
  # for index in range(1,len(ann_files)/3 + 1):
  ann2triples = []
  for index in range(1,278):
    print(index)
    with open("./KG_annotation/%d.puzzle.ann" % index, 'r', encoding='utf-8') as f_puzzle,open('./KG_annotation/%d.truth.ann' % index, 'r', encoding='utf-8') as f_truth:
      # puzzle annotation
      p_Entity, p_Relation, p_Event_relation = Ann2Triples(f_puzzle)
      p_ann2triples = {"Entity": list(set(p_Entity)), "Relation":p_Relation, "Event":p_Event_relation}
      # truth annotation
      t_Entity, t_Relation, t_Event_relation = Ann2Triples(f_truth)
      t_ann2triples = {"Entity": list(set(t_Entity)), "Relation":t_Relation, "Event":t_Event_relation}
      ann2triples.append({"puzzle":p_ann2triples, "truth":t_ann2triples})
    f_puzzle.close()
    f_truth.close()
  # print(ann2triples)
  with open(ann_data_path ,"w",encoding="utf-8") as fd:
      json.dump(ann2triples, fd)
      fd.close()

def solution_ann():
  ann_data_path = "./ann_solution_data_50-60.json"
  # for index in range(1,len(ann_files)/3 + 1):
  ann2triples = []
  for index in range(51,61):
    print(index)
    with open("../brat-1.3p1/data/assign_annotation/solution/%d.solution.ann" % index, 'r', encoding='utf-8') as f_solution:
      # solution annotation
      s_Entity, s_Relation, s_Event_relation = Ann2Triples(f_solution)
      s_ann2triples = {"Entity": list(set(s_Entity)), "Relation":s_Relation, "Event":s_Event_relation}

      ann2triples.append(s_ann2triples)
    f_solution.close()
  # print(ann2triples)
  with open(ann_data_path ,"w",encoding="utf-8") as fd:
      json.dump(ann2triples, fd)
      fd.close()


if __name__=="__main__":
  puzzle_truth_ann()
          
'''
  ({'T1': 'physics professor', 'T2': 'demonstrating', 'T3': 'conservation of energy',
   'T4': 'suspending', 'T5': 'bowling ball', 'T6': 'from a piece of rope',
   'T7': 'pulls', 'T8': 'ball', 'T9': 'back', 
   'T10': 'right in front of', 'T11': 'his nose', 'T12': 'lets go', 
   'T13': 'supposed', 'T14': 'swing away from', 'T15': 'back', 
   'T16': 'stopping', 'T17': 'in front of',
    'T18': 'gave', 'T19': 'a slight push', 'T20': 'crashing into',
    'T21': 'upon its return'}, 
  [
  ['Event_att', 'from a piece of rope', 'suspending'], 
  ['EventTemporal', 'pulls', 'back'], 
  ['EventCause', 'back', 'right in front of'], 
  ['EntityEqual', 'ball', 'bowling ball'], 
  ['EventTemporal', 'right in front of', 'lets go'], 
  ['NC2Event', 'supposed', 'swing away from'], 
  ['EventTemporal', 'swing away from', 'back'],
  ['NC2Event', 'stopping', 'in front of'], 
  ['EventTemporal', 'back', 'stopping'], 
  ['NC2Event', 'gave', 'a slight push'], 
  ['EventCause', 'a slight push', 'crashing into'],
  ['Event_att', 'upon its return', 'crashing into']])
  {'E1': ['T2', 'T1', 'T3'], 
  'E2': ['T4', 'T1', 'T5'], 
  'E3': ['T7', 'T1', 'T8'], 
  'E4': ['T9', 'T8', 'None'],
  'E5': ['T10', 'T8', 'T11'],
  'E6': ['T12', 'T8', 'None'], 
  'E7': ['T13', 'T1', 'Noen'], 
  'E8': ['T14', 'T1', 'None'], 
  'E9': ['T15', 'T8', 'T1'],
  'E10': ['T16', 'T8', 'Noen'],
  'E11': ['T17', 'T11', 'None'],
  'E12': ['T18', 'T1', 'Noen'],
  'E13': ['T19', 'T8', 'None'],
  'E14': ['T20', 'T8', 'T11']}
  [['demonstrating', 'physics professor', None], 
  ['suspending', 'physics professor', None], 
  ['pulls', 'physics professor', None], 
  ['back', 'ball', None], 
  ['right in front of', 'ball', None], 
  ['lets go', 'ball', None], 
  ['supposed', 'physics professor', None], 
  ['swing away from', 'physics professor', None],
   ['back', 'ball', 'physics professor'], 
   ['stopping', 'ball', 'physics professor'], 
   ['in front of', 'his nose', None], 
   ['gave', 'physics professor', None], 
   ['a slight push', 'ball', None], 
   ['crashing into', 'ball', 'his nose']]
   '''