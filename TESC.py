# Name: Johayer Rahman Chowdury
# HW4, Due: Friday Nov 26, 2022
# Program: Topic Evaluation Score Calculator (TESC)
# Purpose: To report the per topic evaluation score (if there are 45 topics, 
# this means you output 45 scores and label them nicely with the topic number) 
# for a given results file and qrels file for the effective measures given:
    # Average Precision, Precision@10, NDCG@10, NDCG@1000, Time-biased gain

from helper_code.parsers import QrelsParser, ResultsParser
import argparse
import math
import csv
from pathlib import Path
import pickle
import time

hw5_5d_jchowdur_csv = Path('hw5-metrics-jchowdur.csv')
hw5_5d_jchowdur_header = ['Run Name', 'Mean Average Precision', 'Mean P@10', 'Mean NDCG@10', 'Mean NDCG@100', 'Mean NDCG@1000', 'Mean TBG']

# Global TBG Variables
prob_click_on_rel_doc = 0.64
prob_click_on_non_rel_doc = 0.39
prob_of_save_rel_doc = 0.77
population_avg_time_summary = 4.4
rate_of_seconds_per_word = 0.018
rate_of_assessing_small_text = 7.8

def calculate_mean(measure):
    average = sum(measure.values()) / len(measure)
    return '{:.3f}'.format(round(average,3))

def write_to_csv(file_path, row, header):
    if not file_path.is_file():
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerow(row)            
    else:
        with open(file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)
        
def print_mean_to_csv(file_author, ap, p_at_10, ndcg_at_10, ndcg_at_100, ndcg_at_1000, tbg):
    mean_ap = calculate_mean(ap)
    mean_p_at_10 = calculate_mean(p_at_10)
    mean_ndcg_at_10 = calculate_mean(ndcg_at_10)
    mean_ndcg_at_100 = calculate_mean(ndcg_at_100)
    mean_ndcg_at_1000 = calculate_mean(ndcg_at_1000)
    mean_tbg = calculate_mean(tbg)

    row = [file_author,mean_ap, mean_p_at_10, mean_ndcg_at_10, mean_ndcg_at_100, mean_ndcg_at_1000, mean_tbg]
    write_to_csv(hw5_5d_jchowdur_csv, row, hw5_5d_jchowdur_header)

def calculate_idcg_at_k(num_qrel_relevant_docs, max_range_value):
    idcg = 0
    # assign k as minimum between the number of relevant docs in qrels and max_range_value
    k = min(num_qrel_relevant_docs, max_range_value)
    for index in range(1,k+1):
        dcg = 1/math.log2(index+1)
        idcg += dcg
    return idcg

def print_statistics(measure, name):
    measure_file = name + '.pkl'
    pickle.dump(measure, open(measure_file,'wb'))

def statistics(qrel, results, file_author, max_results, mapping, doc_lengths):

    # query_ids are same as topic_numbers
    query_ids = sorted(qrel.get_query_ids())
    
    # dictionaries to hold all measures for each topic number
    ap = {}
    precision_at_rank_10 = {}
    ndcg_at_10 = {}
    ndcg_at_100 = {}
    ndcg_at_1000 = {}
    tbg = {}

    for query_id in query_ids:
        print("Now calculating measures for topic number", query_id)
        ### Average Precision variables ###
        # denominator of average precision formula (|R|)
        sum_relevance_judgement = len(qrel.query_2_reldoc_nos[query_id])
        
        # numerator of average precision formula (sum of products of relevance and precision at rank i for result i)
        sum_numerator = 0

        ### NDCG variables ###
        idcg_at_10 = calculate_idcg_at_k(sum_relevance_judgement, 10)
        idcg_at_100 = calculate_idcg_at_k(sum_relevance_judgement, 100)
        idcg_at_1000 = calculate_idcg_at_k(sum_relevance_judgement, 1000)
        dcg_at_10 = 0
        dcg_at_100 = 0
        dcg_at_1000 = 0
        

        ### Time biased gain variables ###
        tbg_num = 0
        # tbg_tk = []
        tbg_tk = 0

        # if a query_id has results
        if results[1].get_result(query_id):
            query_result = sorted(results[1].get_result(query_id))

            sum_relevant_docs_found = 0
            for index, result in enumerate(query_result[:max_results], start=1):

                relevance = qrel.get_relevance(query_id, result.doc_id)
                if relevance != 0:
                    sum_relevant_docs_found += 1
                    prob_click_given_NIST_relevance = prob_click_on_rel_doc
                else:
                    prob_click_given_NIST_relevance = prob_click_on_non_rel_doc

                if index <= 1000:
                    dcg = relevance / math.log2(index+1)
                    dcg_at_1000 += dcg
                    if index <= 100:
                        dcg_at_100 += dcg
                    if index <= 10:
                        dcg_at_10 += dcg
                
                precision_at_rank_n = sum_relevant_docs_found / index
                sum_numerator += (relevance * precision_at_rank_n)
                
                if index == 10:
                    precision_at_rank_10[query_id] = precision_at_rank_n
                
                # gain of time-biased gain
                tbg_gk = relevance * prob_click_on_rel_doc * prob_of_save_rel_doc

                # expected time for user to reach rank k and begin to assess document
                # find doc length
                docno = result.doc_id.replace(' ', '')
                # https://note.nkmk.me/en/python-dict-get-key-from-value/ helped to get key from value in dictionary
                doc_internal_id = [k for k, v in mapping.items() if v == str(docno)][0]
                doc_length = int(doc_lengths[doc_internal_id])

                # decay of time
                decay_of_tbg_tk = math.exp( (-1 * tbg_tk) * (math.log(2) / 224) )
                tbg_num += (tbg_gk * decay_of_tbg_tk)
                tk_i = (population_avg_time_summary + (rate_of_seconds_per_word * doc_length + rate_of_assessing_small_text) * prob_click_given_NIST_relevance)
                tbg_tk += tk_i
                
        else:
            precision_at_rank_10[query_id] = 0

        tbg[query_id] = tbg_num
        ap[query_id] = (sum_numerator / sum_relevance_judgement)
        ndcg_at_10[query_id] = (dcg_at_10 / idcg_at_10)
        ndcg_at_100[query_id] = (dcg_at_100 / idcg_at_100)
        ndcg_at_1000[query_id] = (dcg_at_1000 / idcg_at_1000)

    print_statistics(ap, "AP")
    print_statistics(precision_at_rank_10, "P@10")
    print_statistics(ndcg_at_10, "ndcg_at_10")
    print_statistics(ndcg_at_100, "ndcg_at_100")
    print_statistics(ndcg_at_1000, "ndcg_at_1000")
    print_statistics(tbg, "TBG")    
    print_mean_to_csv(file_author, ap, precision_at_rank_10, ndcg_at_10, ndcg_at_100, ndcg_at_1000, tbg)

def main():
    # Author: Nimesh Ghelani based on code by Mark D. Smucker
    parser = argparse.ArgumentParser(description='Evaluate topic(s) evaluation score for a given results file and qrels file')
    parser.add_argument('--qrel', required=True, help='Path to qrel')
    parser.add_argument('--results', required=True, help='Path to file containing results')
    parser.add_argument('--document-directory', required=True, help='Path to directory containing documents')
    parser.add_argument('--max-results', type=int, help='Max number of results to iterate for each query')

    cli = parser.parse_args()
    qrel_file = QrelsParser(cli.qrel)
    results_file = ResultsParser(cli.results)
    results_file_author = results_file.get_author()
    document_stored_directory = Path(cli.document_directory)

    # get doc_lengths of collection
    doc_lengths_path = document_stored_directory / 'doc_length.pkl'
    doc_lengths = pickle.load(open(doc_lengths_path, 'rb'))

    # get mapping of collection
    mapping_path = document_stored_directory / 'mapping_between_id_and_docno.pkl'
    mapping = pickle.load(open(mapping_path, 'rb'))

    # for acceptable results (and qrels) files
    try:
        qrel = qrel_file.parse()
        results = results_file.parse()
        max_results = 1000
        if cli.max_results:
            max_results = cli.max_results
        # use helper function to calculate statistics using given qrels and results files
        startTimeTotal = time.time()
        print('Now calculating scores for ' + str(Path(cli.results)) + 'using qrels located in ' + str(Path(cli.qrel)) )
        statistics(qrel, results, results_file_author, max_results, mapping, doc_lengths)
        endTimeTotal = time.time()
        print("Total time taken for " + str(Path(cli.results)) + " is: " +  (endTimeTotal-startTimeTotal))

    # for results (and possibily qrels) files that are not acceptable
    except:
        incorrect_format_list = []
        incorrect_format_list.append(results_file_author)
        for i in range(len(hw5_5d_jchowdur_header) - 1):
            incorrect_format_list.append('Bad Format')
        write_to_csv(hw5_5d_jchowdur_csv, incorrect_format_list, hw5_5d_jchowdur_header)

if __name__ == "__main__":
    main()
