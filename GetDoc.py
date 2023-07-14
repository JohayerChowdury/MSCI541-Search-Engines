# Name: Johayer Rahman Chowdury
# HW5, Due: Friday Dec 6, 2022
# Program: GetDoc

import sys
from pathlib import Path

# method that returns month, day, year from DOCNO tag
def process_doc_date(date_text: str):
    date_text = date_text.replace('LA', '')
    month = date_text[:2]
    day = date_text[2:4]
    year = date_text[4:6]
    return month, day, year

def output_docno_path(document_stored_directory:Path, docno: str):
    month, day, year = process_doc_date(docno)
    # documents subdirectory and document files
    doc_file = docno + '.txt.gz'
    doc_metadata_file = docno + '_metadata.txt.gz'
    doc_file_path = document_stored_directory / year / month / day / doc_file
    doc_metadata_file_path = document_stored_directory / year / month / day / doc_metadata_file
    if doc_file_path.exists() and doc_metadata_file_path.exists():
        output = doc_metadata_file_path.read_bytes() + b'\nraw document:\n' + doc_file_path.read_bytes()
        return output.decode()
    elif not doc_file_path.exists() and doc_metadata_file_path.exists():
        print("Document was created but only its metadata was found in directory.")
        return doc_metadata_file_path.read_bytes().decode()
    elif not doc_metadata_file_path.exists() and doc_file_path.exists():
        print("Document was created but metadata was NOT found in directory.")
        output = b'\nraw document:\n' + doc_file_path.read_bytes()
        return output.decode()
    else:
        return "Document not found. Please provide a different docno or id."

def read_paths():
    # read second argument for documents directory
    document_stored_directory = Path(sys.argv[1])

    if not document_stored_directory.exists():
        sys.exit(str(document_stored_directory) + " does not exist :(")

    if sys.argv[2] == 'docno':
        docno = sys.argv[3]
        sys.exit(output_docno_path(document_stored_directory, docno))

    elif sys.argv[2] == 'id':
        id = sys.argv[3]
        mapping_path = document_stored_directory / 'mapping_between_id_and_docno.txt'
        if mapping_path.is_file():
            docno = ''
            with open(mapping_path, 'r') as f1:
                for line in f1:
                    # remove newline characters from line
                    line = line.strip()
                    # example mapping: LA123190-0134 || 329701
                    id_in_mapping = line[17:]
                    if id_in_mapping.isdigit():
                        id_in_mapping = int(id_in_mapping)
                        if id_in_mapping == int(id):
                            docno = line[:13]
                            f1.close()
                            break
            sys.exit(output_docno_path(document_stored_directory, docno))

    else:
        sys.exit('Argument 2 is not either "id" or "docno"')

def main():
    if(len(sys.argv) - 1 < 3):
        sys.exit(
            'One or more arguments are NOT supplied. This program accepts three command line arguments:\n'
            '1. a path to the location of the documents and metadata store created by IndexEngine.py,\n'
            '2. either the string "id" or the string "docno" and,\n'
            '3. either the internal integer id of a document or a DOCNO.'
            )
    elif(len(sys.argv) - 1 > 3):
        sys.exit(
            'Too many arguments are supplied. This program accepts three command line arguments:\n'
            '1. a path to the location of the documents and metadata store created by IndexEngine.py,\n'
            '2. either the string "id" or the string "docno" and,\n'
            '3. either the internal integer id of a document or a DOCNO.'
            )
    else:
        read_paths()
    
if __name__ == "__main__":
    main()