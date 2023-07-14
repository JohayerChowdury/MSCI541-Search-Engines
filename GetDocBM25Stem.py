# Name: Johayer Rahman Chowdury
# HW5, Due: Tuesday Dec 26, 2022
# Program: Find docnos, document text and queries for results (BM25 specifically).

import sys
from pathlib import Path
import xml.etree.ElementTree as ET
import pickle

import GetDoc

def read_paths():
    try:
        bm25_stem_index = Path(sys.argv[2])
    except FileNotFoundError:
        msg = "File " + str(sys.argv[2]) + " does not exist. Please provide correct file."
        sys.exit(msg)
    
    try:
        queries_pickled = Path(sys.argv[3])
    except FileNotFoundError:
        msg = "File " + str(sys.argv[2]) + " does not exist. Please provide correct file."
        sys.exit(msg)

    queries_unpickled = pickle.load(open(queries_pickled,'rb'))
    bm25_stem_results_file = open(sys.argv[1], "r")

    docnos = []
    bm25_stem_results_text = []
    queries = []

    current_topic_number = ''
    for line in bm25_stem_results_file:
        columns = line.split()
        topic_number = columns[0]
        if topic_number != current_topic_number:
            current_topic_number = topic_number
            print('now finding docs for: ', current_topic_number)
        docno = columns[2]
        docnos.append(docno)

        doc = GetDoc.output_docno_path(bm25_stem_index, docno)
        root = ET.fromstring(doc)

        output = ''
        if root.find('HEADLINE'):
            headline = root.findtext('HEADLINE/P').replace('\n', '')
            output += headline
        else:
            headline = 'headline does not exist'

        for text_tag in root.findall('TEXT'):
            for p_tag in text_tag.findall('P'):
                output += p_tag.text
                 
        if root.find('GRAPHIC'):
            graphic = root.findtext('GRAPHIC/P').replace('\n', '')
            output += graphic
        
        output = output.replace('\n', '')
        # print(output)
        bm25_stem_results_text.append(output)
        queries.append(queries_unpickled[topic_number])
    
    docnos_path = 'docnos_for_hw5.pkl'
    pickle.dump(docnos, open(docnos_path, 'wb'))

    docs_path = 'docs_for_hw5.pkl'
    pickle.dump(bm25_stem_results_text, open(docs_path, 'wb'))

    queries_path = 'queries_for_hw5.pkl'
    pickle.dump(queries, open(queries_path, 'wb'))
    
def main():
    if(len(sys.argv) - 1 < 3):
        sys.exit(
            'One or more arguments are NOT supplied. This program accepts three command line arguments:\n'
            '1. a relative path to the BM25 stem results.\n'
            '2. a relative path to the BM25 stem index.\n'
            '3. a relative path to the dictionary of queries.'
            )
    elif(len(sys.argv) - 1 > 3):
        sys.exit(
            'One or more arguments are NOT supplied. This program accepts three command line arguments:\n'
            '1. a relative path to the BM25 stem results.\n'
            '2. a relative path to the BM25 stem index.\n'
            '3. a relative path to the dictionary of queries.'
            )
    else:
        read_paths()
    
if __name__ == "__main__":
    main()