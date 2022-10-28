# project_2022--lateral thinking pipeline
1. situation-data -- orignal text form html
2. data_preprocess.py -- preprocess for situation-data to json
3. test.py -- single example test only for generate
4. puzzle.json -- part of QA dataset
5. answer_predcict.txt and Answer_predict.txt -- first test output
6. example.json -- single example for demo.py
7. demo_set
    demo.py -- QA demo
    new_dataset.json -- after QA the original dataset would be change, it's new dataset that append follow-uo-QA.
    demo1.0.py -- question generation with hint and after QA-G finish generate a solution every turn.
    demo2.0.py -- question generation with hint and after 5 turns QA-G finish then generate a solution. 
    demo1.1.py -- add similarity calculate & example truncation & sleep & after the first turn no more example prompt.