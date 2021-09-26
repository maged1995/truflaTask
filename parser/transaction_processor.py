from posixpath import basename
from parser.xml_parser import XMLParser
from parser.csv_parser import CSVParser
import pandas as pd

def pre_process(filenames, file_type):
    if file_type == 'xml':
        parser = XMLParser(filenames[0])
    elif file_type == 'csv':
        parser = CSVParser(filenames[0], filenames[1])
    parser.pre_process()
    parser.parse_to_json()
