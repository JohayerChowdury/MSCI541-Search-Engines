# hw5-JohayerChowdury
hw5-JohayerChowdury created by GitHub Classroom
MSCI-541-HW5 Johayer Rahman Chowdury

Handed In: December 06, 2022

### To run *IndexEngine*, open the terminal and run 'python IndexEngine.py' with the following arguments:

- absolute/relative path to the latimes.gz file (restricted TREC data)
- absolute/relative path to the directory to store the documents and their metadata
- (optional argument) 0 for no stemming, 1 for stemming

For example:

- python IndexEngine.py ./latimes.gz ./latimes-index

### To run *GetDoc*, open the terminal and run 'python GetDoc.py' with the following arguments:

absolute/relative path to the directory created after running IndexEngine
One of the following words: docno, id
The docno or id of the document based on the word chosen in the previous argument.
For example:

python GetDoc.py ./latimes-index docno LA010389-0090
python GetDoc.py ./latimes-index id 24

### To run *BM25*, open the terminal and run 'python BM25.py' with the following operators and arguments:

- --index-path, 'Path to the directory location of your index'
- --queries-path, 'Path to the queries file'
- --output-path, 'Path to store output in a new file'
- --toStem, type=int, help='Optional argument: 0 for basic tokenization, 1 for stemming in tokenization (default is 0)'

### To run *GetDocBM25stem*, open the terminal and run 'python GetDOCBM25stem.py' with the following operators and arguments:

1. a relative path to the BM25 stem results.
2. a relative path to the BM25 stem index.
3. a relative path to the dictionary of queries.

After running GetDocBM25stem.py, three files will be created. 3 pickled files; 1 that stores the documents' text in a list, 1 that stores the documents' docnos in a list, and 1 that stores the queries associated for that document in a list.

#### To run *monoBERT_ranking_results.py*, use the three files created after running GetDocBM25stem.py in conjunction with the ExtractQueries program that creates a pickled file that stores the dictionary of queries and topic numbers.

### To run *Topic Evaluation Score Calculator (TESC)*, open the terminal and run 'python TESC.py' with the following operators and arguments:

- --qrel Path_to_qrel
- --document-directory Path_to_directory_containing_documents
- --results Path_to_file_containing_results
- (optional) --max-results Max_number_of_results_to_iterate_for_each_query

For example:

- python TESC.py --qrel ../hw3-files/qrels/LA-only.trec8-401.450.minus416-423-437-444-447.txt --document-directory ./latimes-index --results ../hw3-files/results-files/student1.results
- python TESC.py --qrel ../hw3-files/qrels/LA-only.trec8-401.450.minus416-423-437-444-447.txt --document-directory ./latimes-index --results ../hw3-files/results-files/student1.results --max-results 500
