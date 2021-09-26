from posixpath import basename, splitext
from .parser_main import ParserMain
import json

class CSVParser(ParserMain):
    def __init__(self, file_name, file_name2):
        ParserMain.__init__(self, file_name)
        self.file_name2 = file_name2

    def parse_to_json(self, output):
        with open(self.file_name, mode='r') as xml_file:
            new_file_name = splitext(basename(self.file_name))[0] + '.json'
            with open(f"output/csv/{self.time_stamp}_{new_file_name}", "w") as json_file:
                json_file.write(output)
                json_file.close()