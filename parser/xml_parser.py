from posixpath import basename, splitext
from .parser_main import ParserMain

class XMLParser(ParserMain):
    def parse_to_json(self, output):
            new_file_name = splitext(basename(self.file_name))[0] + '.json'
            with open(f"output/csv/{self.time_stamp}_{new_file_name}", "w", encoding='utf-8') as json_file:
                json_file.write(output)
                json_file.close()