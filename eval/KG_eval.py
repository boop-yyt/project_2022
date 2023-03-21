from bleurt import score
import json
def span_score(span1, sapn2):
    scores = 0.0
    if span1 and sapn2:
        scorer = score.BleurtScorer()
        scores = scorer.score(references=[span1], candidates=[sapn2])[0]
    # print(span1," // ", sapn2," // ", scores)
    return scores

def triples_score(triples1, triples2):
    single_score = 0.0
    single_num = 0
    for head_end1 in triples1:
        for head_end2 in triples2:
            single_num += 1
            single_score += span_score(head_end1, head_end2) 
    single_score /= single_num
    # print(triples1," // ", triples2," // ",single_score)
    return single_score 

def Entity_triples_score(triples1,triples2):
    Entity_score = 0.0
    for tp1 in triples1:
        best_entity_score = -100.0
        for tp2 in triples2:
            temp_score = span_score(tp1,tp2)
            if best_entity_score < temp_score:
                best_entity_score = temp_score
        Entity_score += best_entity_score
    Entity_score /= 2
    print("Entity_score",Entity_score)
    return Entity_score

def Relation_triples_score(triples1, triples2):
    Relation_score = 0.0
    for tp1 in triples1:
        best_relation_score = -100.0
        for tp2 in triples2:
            if tp1[0] == tp2[0]:
                temp_score = triples_score(tp1[1:], tp2[1:])
                if best_relation_score < temp_score:
                    best_relation_score = temp_score
        Relation_score += best_relation_score
    Relation_score /= 2
    print("Relation_score",Relation_score)
    return Relation_score

def Event_triples_score(triples1,triples2):
    Event_score = 0.0
    for tp1 in triples1:
        best_event_score, best_node_score = -100.0, -100.0
        for tp2 in triples2:
            temp_event_score = span_score(tp1[0], tp2[0])
            temp_node_score = triples_score(tp1[1:], tp2[1:])
            if best_event_score < temp_event_score:
                best_event_score = temp_event_score
                best_node_score = temp_node_score
        Event_score += best_event_score
        Event_score += best_node_score
    Event_score /= 2
    print("Event_score",Event_score)
    return Event_score

def text_triples_score(text_triples1, text_triples2):
    W_en, W_re, W_ev = 0.33, 0.33, 0.33
    Entity_score = Entity_triples_score(text_triples1["Entity"], text_triples2["Entity"])
    print("**************relation_score*********************")
    Relation_score = Relation_triples_score(text_triples1["Relation"], text_triples2["Relation"])
    print("**************event_score*********************")
    print(text_triples1["Event"], text_triples2["Event"])
    Event_score = Event_triples_score(text_triples1["Event"], text_triples2["Event"])
    final_score = W_en * Entity_score + W_re * Relation_score + W_ev * Event_score
    return final_score

def truth_solution_KGscore():
    # truth_file, solution_file = "./data/ann_data.json","./data/solution_ann.json"
    truth_file, solution_file = "../data/ann_data.json","solution.json"
    with open(truth_file,"r",encoding="utf-8") as ft, open(solution_file,"r",encoding="utf-8") as fsl:
        truth_set = json.load(ft)
        solution_set = json.load(fsl)
    ft.close()
    fsl.close()
    final_score, total_KG_score, each_score_lsit = 0.0, 0.0, []
    for titem, sitme in zip(truth_set[50:61], solution_set):
        KG_score = text_triples_score(titem["truth"], sitme)
        each_score_lsit.append(KG_score)
        print("KG_score:", KG_score)
        total_KG_score += KG_score
    final_score = total_KG_score / len(each_score_lsit)
    final_score /= 2
    print("*",final_score)


def stand_KGscore():
    # truth_file, solution_file = "./data/ann_data.json","./data/solution_ann.json"
    truth_file = "../data/ann_data.json"
    with open(truth_file,"r",encoding="utf-8") as ft:
        truth_set = json.load(ft)
    ft.close()
    final_score, total_KG_score, each_score_lsit = 0.0, 0.0, []
    for titem in truth_set:
        print("$$$$:",titem["truth"])
        KG_score = text_triples_score(titem["truth"], titem["truth"])
        each_score_lsit.append(KG_score)
        print("KG_score:", KG_score)
        total_KG_score += KG_score
    final_score = total_KG_score / len(each_score_lsit)
    final_score /= 2
    print("*",final_score)

if __name__=="__main__":
    # stand_KGscore()
    truth_solution_KGscore()
    
