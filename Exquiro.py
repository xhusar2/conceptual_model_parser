#!/usr/bin/python3
import getopt
import os
import sys

from Neo4jManager import Neo4jManager
from Parser import parse_file


def parse_args(argv):
    input_file = ''
    directory = ''
    try:
        opts, args = getopt.getopt(argv, "hi:d:", ["ifile=", "directory="])
    except getopt.GetoptError:
        print('test.py -i <input_file> -d <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <input_file> -d <output_file>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-d", "--directory"):
            directory = arg
    return input_file, directory


# open xmi file
def main(argv):
    input_file, directory = parse_args(argv)
    neo4j_manager = Neo4jManager()
    # delete earlier graphs
    neo4j_manager.delete_all()

    if input_file != '':
        print('Input file is ', input_file)
        # parse file
        parsed_m = parse_file(input_file)
        neo4j_manager.add_to_db(parsed_m)

    elif directory != '':
        path = os.walk(directory)
        for root, directories, files in path:
            for file in files:
                if str(file).endswith('.xml') or str(file).endswith('.xmi'):
                    file_path = os.path.join(directory, file)
                    parsed_model = parse_file(file_path)
                    try:
                        print("model name:", parsed_model.id)
                        neo4j_manager.add_to_db(parsed_model)
                    except:
                        print(f'could not parse model from file {file}')


# check if it is XMI format

# parse model

# TODO openPonk format parsing: types and properties
# TODO git connector

if __name__ == "__main__":
    main(sys.argv[1:])
