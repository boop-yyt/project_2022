from selectolax.parser import HTMLParser
import os
# html_file = "./chat.html"
def preprocess(str):
    str=str.replace('\n','')  #去除换行
    # print(str)
    newstr=''
    newlist=str.split(' ')  #按空格拆分，连续空格拆出来为''，否则就是单词
    n=len(newlist)
    # 合并
    for i in range(n):
        if newlist[i]!='':
            newstr+=newlist[i]
            if i != n - 1:
                newstr += ' '
    return newstr

def html_text(html_file):
    text_list = []
    with open(html_file,"r", encoding="utf-8") as f:
        html = f.read() 

    tree = HTMLParser(html)
    for tag in tree.css('div[class]'):
        value = tag.attributes["class"]
        # print(value)
        if value == "markdown prose w-full break-words dark:prose-invert light":
            text = tag.text()
            formatted_text = preprocess(text)
            # formatted_text = text.replace("                                                            ", "").replace("\n"," ")
            # formatted_text = text.replace("\n", "").replace("\n", "\t")
            # formatted_text = "".join(text.split("\n"))
            # print(formatted_text)
            text_list.append(formatted_text)
    return text_list

html_file = "./html-output/chat_wo_puzzle_193.html"
item_text_list = html_text(html_file)
with open("./html-output/output_wo_puzzle_193.txt", "a", encoding="utf-8") as f:
            for item in item_text_list:
                f.write(item+"\n")
f.close()
# if __name__ =='__main__':
#     html_path = "./chat_html"
#     # output_text ="./chat_html/output.txt"
#     html_files= os.listdir(html_path)
#     index = 0
#     for file in html_files:
#         index += 1
#         print(file)
#         html_file = "./chat_html/"+file
#         item_text_list = html_text(html_file)
#         with open("./chat_html/output_%d.txt"%index, "a", encoding="utf-8") as f:
#         # with open(output_67_84.txt, "a", encoding="utf-8") as f:
#             for item in item_text_list:
#                 f.write(item+"\n")
#         f.close()
  