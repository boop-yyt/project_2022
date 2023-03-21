import json
from Answer import load_data

# 对solution和truth进行三元组评估
'''
similarity(E_s,E_T)=Score(E_s,E_T)
similarity(ET_s,ET_T)=Score(ET_s,ET_T)
'''
truth_triples = {
            "Entity": [ "abalone","what", "man's wife","they","there", "his wife","he",
                "food", "himself","civilization","a desert island","another passenger", "ship",
                "man"
            ],
            "Relation": [
                ["EntityEqual","a desert island","there"],
                ["Entity_att","he said","what"],
                ["EntityEqual","abalone","what"],
                ["EntityPartof", "what","man's wife"],
                ["EventEqual","wrecked on","wreck"],
                ["EventCause", "wreck", "had died in"],
                ["EntityPartof","man","they"],
                ["EntityPartof","another passenger", "they"],
                ["EntityEqual","man", "man"],
                ["NC2Event","realizes","ate"],
                ["EventTemporal","realizes","kills"],
                [ "EntityEqual","man's wife","his wife"],
                ["EntityEqual", "he", "he"],
                ["EntityEqual","man", "he"]
            ],
            "Event": [
                [ "in", "man",null],
                ["wrecked on", "ship","a desert island"],
                ["left",null,null],
                ["brought","another passenger",null],
                ["had died in","man's wife",null],
                ["wreck",null,null],
                [ "suspects","man",null],
                ["return","they",null],
                ["orders","he",null],
                ["realizes","he",null],
                ["ate",null,null],
                [ "kills", "he", null]
            ]
        }
def word2vec(datafile):
  model  = Word2Vec(
    LineSentence(open(datafile, "r", encoding="utf-8")),
    sg=0,
    vector_size=50,
    window=3,
    min_count=1,
    workers=8
  )
  model.wv.save_word2vec_format("./data.vec", binary=False)
  model.save("./vec.model")
  # print(model.wv['people','person'])
  return model

import numpy as np
from scipy import spatial
 
index2word_set = set(model.index2word)
 
def avg_feature_vector(triples, model, num_features, index2word_set):
    words = 
    for el in triples:
      el = el.split()
    words = sentence.split()
    feature_vec = np.zeros((num_features, ), dtype='float32')
    n_words = 0
    for word in words:
        if word in index2word_set:
            n_words += 1
            feature_vec = np.add(feature_vec, model[word])
    if (n_words > 0):
        feature_vec = np.divide(feature_vec, n_words)
    return feature_vec
