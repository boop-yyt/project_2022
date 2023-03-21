from bleurt import score
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '6'

checkpoint = "../../BLEURT-20"
scorer = score.BleurtScorer(checkpoint)

bleurt_text_score = scorer.score(
    references=["The vet could see that the goldfish was dying of old age so to spare the old lady's feelings he dashed out and bought a young but identical fish and disposed of the old one."], 
    candidates=["Without more information, it is impossible to determine why the man took off and put on a glove in the elevator. There could be many reasons why the man might have done this, and it is impossible for me to speculate on the specific c reason in this situation. lt is important to remember that people's actions and behavior can be influenced by a wide range of factors, and it is not always possible to understand the reasons behind someone's actions without knowing more about the individual and their circumstances. "]
    )
print(bleurt_text_score)
