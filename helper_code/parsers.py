
from helper_code.Qrels import Qrels, Judgement
from helper_code.Results import Results, Result
from pathlib import Path

# Author: Nimesh Ghelani based on code by Mark D. Smucker
# modified for this homework assignment

class ResultsParseError(Exception):
    pass

class ResultsParser:

    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        global_run_id = None
        history = set()
        results = Results()
        with open(self.filename) as f:
            for line in f:
                line_components = line.strip().split()
                if len(line_components) != 6:
                    raise ResultsParseError('lines in results file should have exactly 6 columns')

                query_id, _, doc_id, rank, score, run_id = line_components
                rank = int(rank)
                score = float(score)

                if global_run_id is None:
                    global_run_id = run_id
                elif global_run_id != run_id:
                    raise ResultsParseError('Mismatching runIDs in results file')

                key = query_id + doc_id
                if key in history:
                    raise ResultsParseError('Duplicate query_id, doc_id in results file')
                history.add(key)

                results.add_result(query_id, Result(doc_id, score, rank))

        return global_run_id, results
    
    def get_author(self):
        path = Path(self.filename)
        return path.stem

class QrelsParseError(Exception):
    pass

class QrelsParser:

    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        qrels = Qrels()
        with open(self.filename) as f:
            for line in f:
                line_components = line.strip().split()
                if len(line_components) != 4:
                    raise QrelsParseError("Line should have 4 columns")
                query_id, _, doc_id, relevance = line_components
                relevance = int(relevance)
                qrels.add_judgement(Judgement(query_id, doc_id, relevance))
        return qrels

