import os
import openai
import json
openai.api_key = os.getenv("OPENAI_API_KEY")
filename = "./qa.json"
# out_filename= "./Lateral/Answer_predict.txt"
discrib_prompt = "I am a chatbot that can answer questions from users based on scenario information."

with open(filename) as datafile:
  data_set = json.load(datafile)
  for data in data_set.values():
    s, q = "".join(data["senario"]), data["question"]
    # a = "A:"+"".join(data["answer"])
    final_prompt = discrib_prompt+"\nscenario:"+s+"\nQ:"+q+"\nA:"
    # final_prompt = discrib_prompt+"\n"+s+"\n"+q+"\n"
    # print(final_prompt)
    # final_prompt = discrib_prompt+"\n\n"+s+"\n"+q+"\n"
    response = openai.Completion.create(
      model="text-davinci-002",
      prompt=final_prompt,
      temperature=0,
      max_tokens=150,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=["\n\n"]
    )
    print(response)
    # print(response.get("choices")[0]["text"])
