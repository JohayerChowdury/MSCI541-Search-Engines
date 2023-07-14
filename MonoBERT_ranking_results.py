# Name: Johayer Rahman Chowdury
# HW5, Due: Tuesday Dec 26, 2022
# Program: Rank scores provided by monoBERT to output TREC ranked results.

import pickle
from collections import defaultdict

def ranking(topics_dict, resultsFilePath):
    with open(resultsFilePath, 'a') as f:
        runTag = "jchowdurBERT"
        for topic in topics_dict:
            rank = 1
            sort_results_by_score = sorted(topics_dict[topic], key=lambda tup: tup[1], reverse=True)
            for result in sort_results_by_score:
                f.write(str(topic) + ' Q0 ' + str(result[0]) + ' ' + str(rank) + ' ' + str(result[1]) + ' ' + str(runTag) + '\n')
                rank += 1
        f.close()

def test_ranking(topics_dict):
    for topic in topics_dict:
        sort_results_by_score = sorted(topics_dict[topic], key=lambda tup: tup[1], reverse=True)
        for result in sort_results_by_score:
            print(str(topic) + ' ' + str(result[0]) + ' ' + str(result[1]))

monobert_scores = pickle.load(open('monobert_scores.pkl','rb'))
queries_topic_number_dict = pickle.load(open('queries.pkl', 'rb'))
queries_text = pickle.load(open('queries_for_hw5.pkl', 'rb'))
docnos = pickle.load(open('docnos_for_hw5.pkl', 'rb'))

topics_dict = defaultdict(list)
for docno, query, score in zip(docnos, queries_text, monobert_scores):
    result = [docno, score]
    topic_number_text = [topic_number for topic_number, query_text in queries_topic_number_dict.items() if query_text == query]
    topic_number = int(topic_number_text[0])
    topics_dict[int(topic_number)].append(result)

ranking(topics_dict, 'hw5-BERT-jchowdur.txt')

