#!/usr/bin/python3
import getopt
import os
import sys

from parsers.ParserFactory import ParserFactory
from Neo4jManager import Neo4jManager
from XMIFile import XMIFile

from parsers.EnterpriceArchitectParsers.EAClsDiagramParser import EaClsDiagramParser

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
    factory = ParserFactory()
    factory.register_parser('enterprise_architect', 'class_diagram', EaClsDiagramParser)

    if input_file != '':
        print('Input file is ', input_file)
        # parse file
        xmi_file = XMIFile(input_file)
        diagrams = xmi_file.get_diagrams()
        for diagram in diagrams:
            parser = factory.get_parser(diagram)
            parsed_models = parser.parse_file(input_file)
            for parsed_model in parsed_models:
                try:
                    # print("model name:", parsed_model.id)
                    neo4j_manager.add_to_db(parsed_model)
                except:
                    print(f'could not parse model from file {input_file}')

    elif directory != '':
        path = os.walk(directory)
        for root, directories, files in path:
            for file in files:
                if str(file).endswith('.xml') or str(file).endswith('.xmi'):
                    file_path = os.path.join(directory, file)
                    xmi_file = XMIFile(file_path)
                    diagrams = xmi_file.get_diagrams()

                    for diagram in diagrams:
                        #try:
                        parser = factory.get_parser(xmi_file.get_format(), diagram)
                        parsed_model = parser.parse_file(file_path)

                        print("model name:", parsed_model.id)
                        neo4j_manager.add_to_db(parsed_model)
                        #except ValueError:
                        #    print(f'could not parse model from file {file}: {ValueError}')
                        #except:
                         #   print(f'could not parse model from file {file}')




if __name__ == "__main__":
    main(sys.argv[1:])
