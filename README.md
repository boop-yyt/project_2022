# project_2022--pipeline
1. situation-data -- orignal text form html
2. data_preprocess.py -- preprocess for situation-data to json
3. Ann2Triples.py -- annotation txt to triples
4. puzzle.json -- part of QA dataset
5. answer_predcict.txt and Answer_predict.txt -- first test output
6. example.json -- single example for demo.py
7. demo_set
    new_dataset.json -- after QA the original dataset would be change, it's new dataset that append follow-uo-QA. 
    output.txt -- chance_count & real_answer(R) & generate_answer(G)  
    demo.py -- QA demo  
    demo1.0.py -- with hint.  
    demo1.1.py --example truncation & after the first turn no more example prompt & with hint.  
    demo1.2.py --example truncation & after the first turn no more example prompt.    
    demo2.0.py -- question generation with hint and after 5 turns QA-G finish then generate a solution.     
8. Experiment  
    shuffleQA -- test QA sequence influence
    demo_bleu -- unified similarity calculation method -- bleu
    demo_edit -- unified similarity calculation method -- edit distance
9. out  
    out.txt -- QA pipline  
    output.txt -- final_answer & genrating answer
10. KG_annotation  
    brat-1.3p1 -- annotate tools 
11. KG with GPT 
    Questioner.py -- comparing truth KG and question KG, give a "yes/no/irrelevant" answer back
    Answer.py -- ask question and final solution generate
    main.py -- pipiline with KG 
    SentParse.py -- converge sents to triples
    