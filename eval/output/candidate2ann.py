import json


if __name__=="__main__":
    candidates_path = "./candidates.txt"
    for index, line in enumerate(open(candidates_path, 'r'), 1):
        with open('./solution/%d.solution.txt' % (index+50), 'w') as tmp:
            tmp.write(line)
        with open('./solution/%d.solution.ann' % (index+50), 'w') as f:
            f.close()
