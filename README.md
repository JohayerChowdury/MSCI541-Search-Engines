# hw4-JohayerChowdury
hw4-JohayerChowdury created by GitHub Classroom

MSCI-541-HW4 Johayer Rahman Chowdury

Handed In: November 25, 2022

To run IndexEngine, open the terminal and run 'python IndexEngine.py' with the following arguments:

- absolute/relative path to the latimes.gz file
- absolute/relative path to the directory to store the documents and their metadata
- (optional argument) 0 for no stemming, 1 for stemming

For example:

- python IndexEngine.py ./latimes.gz ./latimes-index

To run BM25, open the terminal and run 'python TESC.py' with the following operators and arguments:

- --index-path, 'Path to the directory location of your index'
- --queries-path, 'Path to the queries file'
- --output-path, 'Path to store output in a new file'
- --toStem, type=int, help='Optional argument: 0 for basic tokenization, 1 for stemming in tokenization (default is 0)'

To run Topic Evaluation Score Calculator (TESC), open the terminal and run 'python TESC.py' with the following operators and arguments:

- --qrel Path_to_qrel
- --document-directory Path_to_directory_containing_documents
- --results Path_to_file_containing_results
- (optional) --max-results Max_number_of_results_to_iterate_for_each_query

For example:

- python TESC.py --qrel ../hw3-files/qrels/LA-only.trec8-401.450.minus416-423-437-444-447.txt --document-directory ./latimes-index --results ../hw3-files/results-files/student1.results
- python TESC.py --qrel ../hw3-files/qrels/LA-only.trec8-401.450.minus416-423-437-444-447.txt --document-directory ./latimes-index --results ../hw3-files/results-files/student1.results --max-results 500
