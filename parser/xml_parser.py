from posixpath import basename, splitext
from .parser_main import ParserMain
from .utils import without_keys
import xmltodict
import json

class XMLParser(ParserMain):
    def pre_process(self):
        with open(self.file_name, mode='r') as xml_file:
            data_dict = xmltodict.parse(xml_file.read(), encoding='utf-8')
            xml_file.close()
            customer_data = data_dict["Insurance"]["Transaction"]["Customer"]
            customer_exclude_data = {"Units"}
            json_res = {
                "file_name": basename(self.file_name),
                "transaction": [
                    {
                        "date": data_dict["Insurance"]["Transaction"]["Date"],
                        "customer": without_keys(customer_data, customer_exclude_data),
                        "Vehicles": customer_data["Units"]["Auto"]["Vehicle"]
                    }
                ]
            }
            self.json_data = json.dumps(json_res, indent=3, ensure_ascii=False).replace("@", "")

    def parse_to_json(self):
            new_file_name = splitext(basename(self.file_name))[0] + '.json'
            with open(f"output/xml/{self.time_stamp}_{new_file_name}", "w", encoding='utf-8') as json_file:
                json_file.write(self.json_data)
                json_file.close()