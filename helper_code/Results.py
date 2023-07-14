# Given by HW3 sources, to store a results file into a Python object
# added my own comments for self-learning

from collections import defaultdict

class Result:
    # store the relevant data of a row of a results file
    def __init__(self, doc_id, score, rank):
        self.doc_id = doc_id
        self.score = score
        self.rank = rank

    # sorts DESC scores of results (ASC ranks of results)
    def __lt__(self, x):
        # return statement given
        return (self.score, self.doc_id) > (x.score, x.doc_id)
    
    def __str__(self):
        return "[DOCID:" + str(self.doc_id) + " SCORE: " + str(self.score) + " RANK: " + str(self.rank) + "]"

class Results:
    def __init__(self):
        self.query_2_results = defaultdict(list)

    def add_result(self, query_id, result):
        self.query_2_results[query_id].append(result)

    def get_result(self, query_id):
        return self.query_2_results.get(query_id, None)

