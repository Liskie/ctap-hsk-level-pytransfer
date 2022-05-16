import requests
import time
import json
from utils import read_text, ssplit
import csv
import re


def mkHSK(path):
    HSKlist = dict()
    '''******'''
    pathHSKList = path
    with open(pathHSKList) as HSKlistfh:
        HSKlist = json.load(HSKlistfh)
        print("Succeedful read the HSK list")
    return HSKlist


def querying(query1):
    query1 = query1.replace("%", "%25")
    query1 = query1.replace("&", "%26")
    query1 = query1.replace("?", "%3F")
    query1 = query1.replace("+", "%2B")
    query1 = query1.replace("/", "%2F")
    query1 = query1.replace("=", "%3D")
    query1 = query1.replace("#", "%23")


    url_base = "http://202.112.194.62:8085/api/execute/pattern"
    url = url_base + "?odinsonQuery=" + query1 + "&pageSize=1000000"

    start = time.time()
    r = requests.get(url)
    endSearch = time.time()

    results_dict_query1 = json.loads(r.text)
    endLoad = time.time()

    print("Search time " + query1 + ": "+str(endSearch-start))
    print("Search num:" + str(results_dict_query1["totalHits"]))
    print("Load time: "+str(endLoad-endSearch))
    return results_dict_query1


def analysis(query, num_rule):
    results_dict_query = querying(query)
    for result in results_dict_query["scoreDocs"]:
        id = result["documentId"].split("/")[-1].split(".")[0]
        results[id][0] += 1
        if(num_rule not in results[id][1]):
            results[id][1].append(num_rule)

    example = [query]
    for result in results_dict_query["scoreDocs"][0:50]:
        example.append("".join(result["words"]))

    return example


def subtraction(query1, query2):
    results_dict_query1 = querying(query1)
    results_dict_query2 = querying(query2)

    print("len " + query1+": "+str(len(results_dict_query1["scoreDocs"])))
    print("len " + query2+": "+str(len(results_dict_query2["scoreDocs"])))

    results1_dict = []
    results2_dict = []
    results = []
    for results1 in results_dict_query1["scoreDocs"]:
        results1_dict.append(
            [results1["sentenceId"], "".join(results1['words'])])
    for results2 in results_dict_query2["scoreDocs"]:
        results2_dict.append(
            [results2["sentenceId"], "".join(results2['words'])])


    for results1 in results1_dict:
        if results1 not in results2_dict:
            results.append(results1)
    return results


inputfile = "hsk_essay_revised_with_meta_20210109_fxz.json"
# print("processing " + inputfile)
with open(inputfile, "r", encoding="utf-8") as f:
    # print(type(f))  # <class '_io.TextIOWrapper'>  也就是文本IO类型
    DOCs = json.load(f)

results = {}
for DOC in DOCs:
    id = DOC['id']
    headline = DOC['作文标题']
    num_char = DOC['字数']
    num_word = DOC['词数']
    country = DOC['国籍']
    level = DOC['证书级别']
    date = DOC['考试日期']
    score_writing = DOC['作文分数']
    texts = DOC['修改']

    if(score_writing == "" or score_writing == "0"or score_writing == "8"):
        continue

    results[id] = [0, [], score_writing, country,
                   headline, level, date]  # 总频次，出现了哪些语言点


def main():
    for hsk_level in ["凝固式"]:
        text_path = hsk_level+".txt"
        rules = []
        for text in read_text(text_path):
            rules.append(text)

        output_file_name = text_path.split(".")[0]
        output_file_name = "results/"+output_file_name+".csv"
        csvFile = open(output_file_name, "w", encoding="utf-8-sig", newline='')
        writer = csv.writer(csvFile)  # 创建写的对象

        output_file_name = text_path.split(".")[0]
        output_file_name = "results/"+output_file_name+"example.csv"
        csvFile = open(output_file_name, "w", encoding="utf-8-sig", newline='')
        writer_example = csv.writer(csvFile)  # 创建写的对象

        num_rule = 0
        for rule in rules:
            print(rule)
            example = analysis(rule.replace('\xa0', ''), num_rule)
            writer_example.writerow(example)
            num_rule += 1
        for id in results.keys():
            writer.writerow(["id"+id,   results[id][0], len(results[id][1]), results[id]
                            [2], results[id][3], results[id][4], results[id][5], results[id][6]])


if __name__ == '__main__':
    main()
