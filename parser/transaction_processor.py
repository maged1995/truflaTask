from parser.xml_parser import XMLParser


from posixpath import basename
from .utils import without_keys
import json
import xmltodict

def pre_process(filename, file_type):
    if file_type == 'xml':
        pareser = XMLParser(filename)
        with open(pareser.file_name, mode='r') as xml_file:
            data_dict = xmltodict.parse(xml_file.read(), encoding='utf-8')
            xml_file.close()
            customer_data = data_dict["Insurance"]["Transaction"]["Customer"]
            customer_exclude_data = {"Units"}
            json_res = {
                "file_name": basename(pareser.file_name),
                "transaction": [
                    {
                        "date": data_dict["Insurance"]["Transaction"]["Date"],
                        "customer": without_keys(customer_data, customer_exclude_data),
                        "Vehicles": customer_data["Units"]["Auto"]["Vehicle"]
                    }
                ]
            }
            json_data = json.dumps(json_res, indent=3, ensure_ascii=False).replace("@", "")
            pareser.parse_to_json(json_data)
            