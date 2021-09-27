from posixpath import basename
from parser.xml_parser import XMLParser
from parser.csv_parser import CSVParser
from pymongo import MongoClient
from decouple import config
import json

def process(filenames, file_type):
    if file_type == 'xml':
        parser = XMLParser(filenames[0])
    elif file_type == 'csv':
        parser = CSVParser(filenames[0], filenames[1])
    if parser.errors: 
        for e in parser.errors: print(e)
    else:
        json_res = parser.pre_process()
        parser.parse_to_json()
        save_to_db(json_res, file_type)

def save_to_db(result, file_type):
    DB_NAME = config('DB_NAME')
    DB_USERNAME = config('DB_USERNAME')
    DB_PASSWORD = config('DB_PASSWORD')
    
    myclient = MongoClient('mongodb://localhost:27017/',
                      username=DB_USERNAME,
                      password=DB_PASSWORD,
                      authSource=DB_NAME,
                      authMechanism='SCRAM-SHA-1')

    mydb = myclient[DB_NAME]

    mycol = mydb[file_type]
    print(json.dumps(result, indent=3, ensure_ascii=False))
    x = mycol.insert_one(result)

