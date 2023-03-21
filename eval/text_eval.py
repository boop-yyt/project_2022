from bleurt import score
import json

def ref_cand_score(output_file):
    ref_path, cand_path = "./output/references_kg50_100.txt", "./output/candidates_kg50_100.txt"
    with open(output_file, 'r',encoding="utf-8") as f:
        data_set = json.load(f)
    # print(data_set[0])
    f.close()
    scorer = score.BleurtScorer()
    final_score, total_score, score_list = 0.0, 0.0, []
    # scores = scorer.score(references=references, candidates=candidates)
    with open(ref_path, 'a+',encoding="utf-8") as fref, open(cand_path, "a+", encoding="utf-8") as fcand:
        for ditem in data_set:
            truth_ref = ditem["final_answer"]
            solution_cand = ditem["solution_list"][-1]
            single_score = scorer.score(references=[truth_ref], candidates=[solution_cand])[0]
            score_list.append(single_score)
            total_score += single_score
            fref.write(truth_ref + "\n")
            fcand.write(solution_cand + "\n")
    fref.close()
    fcand.close()
    final_score = total_score / len(score_list)
    return final_score

def stand_score(output_file):
    # ref_path, cand_path = "./output/references_kg.txt", "./output/candidates_kg.txt"
    with open(output_file, 'r',encoding="utf-8") as f:
        data_set = json.load(f)
    # print(data_set[0])
    f.close()
    scorer = score.BleurtScorer()
    final_score, total_score, score_list = 0.0, 0.0, []
    # scores = scorer.score(references=references, candidates=candidates)
    # with open(ref_path, 'a+',encoding="utf-8") as fref, open(cand_path, "a+", encoding="utf-8") as fcand:
    for ditem in data_set:
        truth_ref = ditem["final_answer"]
        # solution_cand = ditem["final_answer"]
        single_score = scorer.score(references=[truth_ref], candidates=[truth_ref])[0]
        score_list.append(single_score)
        total_score += single_score
            # fref.write(truth_ref + "\n")
            # fcand.write(solution_cand + "\n")
    # fref.close()
    # fcand.close()
    final_score = total_score / len(score_list)
    return final_score


if __name__ =='__main__':
    # standard bleurt
    # output_file_kg = "../data/lateral_data.json"
    # final_score = stand_score(output_file_kg)
    # print("stand_score_277 ", final_score)
    # GPT_GPT
    # output_file = "../demo_set/output/final_data_output_101-149.json"
    # final_score = ref_cand_score(output_file)
    # print(final_score)
    # KG_GPT
    output_file_kg = "../KG_with_GPT/output/KG_final_data_output_50_100.json"
    final_score = ref_cand_score(output_file_kg)
    print(final_score)


            


