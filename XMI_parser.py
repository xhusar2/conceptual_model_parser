#!/usr/bin/python3

import os
import sys, getopt

from model.Model import Model
from Neo4j_parser import Model_parser

#open xmi file
def main(argv):
   inputfile = ''
   dir = ''
   try:
      opts, args = getopt.getopt(argv,"hi:d:",["ifile=","directory="])
   except getopt.GetoptError:
      print('test.py -i <inputfile> -d <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('test.py -i <inputfile> -d <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-d", "--directory"):
         dir = arg
   if inputfile != '':
      print('Input file is ', inputfile)
      m = Model("model_1", inputfile)
      m.parse_model()
      n_parser = Model_parser(m)
      n_parser.delete_all()
      n_parser.parse()
   elif dir != '':
      path = os.walk(dir)
      models = []
      for root, directories, files in path:
         for file in files:
            print(file)
            if str(file).endswith('.xml'):
               models.append(Model(file, os.path.join(dir, file)))

      neo4j_parser = Model_parser()
      neo4j_parser.delete_all()
      for m in models:
         print(m.name)
         neo4j_parser.add_to_db(m)








#check if it is XMI format

#parse model

#TODO









if __name__ == "__main__":
   main(sys.argv[1:])