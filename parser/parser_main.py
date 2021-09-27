import time

class ParserMain:
    def __init__(self, file_name):
        self.file_name = file_name
        self.time_stamp = time.time()
        self.exceptions = set()
        self.errors = set()

    def enrich_data(self, **kwargs):
        pass

    def pre_process(self):
        pass

    def parse_to_json(self):
        pass
