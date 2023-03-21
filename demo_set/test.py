# from nltk.translate.bleu_score import sentence_bleu
import sacrebleu
# from sacrebleu.metrics import BLEU

sen1 = "The man had a rare condition where the slightest touch to his skin would cause him to go into anaphylactic shock and die. The abalone was the trigger."
sen2 = "The man was a Japanese businessman. In Japan, it is considered very rude to leave food on your plate, so the man felt he had no choice but to eat the abalone even though he did not like it."
similarity_score_shuffle = sacrebleu.sentence_bleu(sen1, [sen2])
print(similarity_score_shuffle)

similarity_score_shuffle = sacrebleu.corpus_bleu(sen1, [sen2])
# similarity_score_shuffle = BLEU.sentence_score(sen1, sen2)

print(similarity_score_shuffle)
print([sen2])
print([[sen2]])
# similarity_score_shuffle = sentence_bleu(sen1.split(), sen2[0].split(),weights=(1,0,0,0))
# print(similarity_score_shuffle)
# similarity_score_shuffle = sentence_bleu(sen1.split(), sen2[0].split(),weights=(0,1,0,0))
# print(similarity_score_shuffle)
# similarity_score_shuffle = sentence_bleu(sen1.split(), sen2[0].split(),weights=(0,0,1,0))
# print(similarity_score_shuffle)
# similarity_score_shuffle = sentence_bleu(sen1.split(), sen2[0].split(),weights=(0,0,0,1))
# print(similarity_score_shuffle)
'''
            # nltk bleu
            similarity_score = sentence_bleu("".join(ditem["final_answer"]).split(),generated_solution.split(), weights=(1,0,0,0))
            all_score["nltk_BLEU1"] = similarity_score
            # print("nltk_BLEU1 score is : ", similarity_score)
            similarity_score = sentence_bleu("".join(ditem["final_answer"]).split(),generated_solution.split(), weights=(0.5,0.5,0,0))
            all_score["nltk_BLEU2"] = similarity_score
            # print("nltk_BLEU2 score is : ", similarity_score)
            similarity_score = sentence_bleu("".join(ditem["final_answer"]).split(),generated_solution.split(), weights=(0.33,0.33,0.33,0))
            all_score["nltk_BLEU3"] = similarity_score
            # print("nltk_BLEU3 score is : ", similarity_score)
            similarity_score = sentence_bleu("".join(ditem["final_answer"]).split(),generated_solution.split(), weights=(0.25,0.25,0.25,0.25))
            all_score["nltk_BLEU4"] = similarity_score
            # print("nltk_BLEU4 score is : ", similarity_score)
            '''