from posixpath import basename
from .utils import without_keys
from parser.xml_parser import XMLParser
from parser.csv_parser import CSVParser
import pandas as pd
import json
import xmltodict

def pre_process(filenames, file_type):
    if file_type == 'xml':
        parser = XMLParser(filenames[0])
        with open(filenames[0], mode='r') as xml_file:
            data_dict = xmltodict.parse(xml_file.read(), encoding='utf-8')
            xml_file.close()
            customer_data = data_dict["Insurance"]["Transaction"]["Customer"]
            customer_exclude_data = {"Units"}
            json_res = {
                "file_name": basename(filenames[0]),
                "transaction": [
                    {
                        "date": data_dict["Insurance"]["Transaction"]["Date"],
                        "customer": without_keys(customer_data, customer_exclude_data),
                        "Vehicles": customer_data["Units"]["Auto"]["Vehicle"]
                    }
                ]
            }
            json_data = json.dumps(json_res, indent=3, ensure_ascii=False).replace("@", "")
            parser.parse_to_json(json_data)
    elif file_type == 'csv':
        parser = CSVParser(filenames[0], filenames[1])
        data1 = pd.read_csv(filenames[0])
        data2 = pd.read_csv(filenames[1])
        data1['owner_id'] = data1.pop('id')
        full_data = pd.merge(data1,data2,on='owner_id').sort_values(by=['owner_id'])
        json_res = { "file_name": f"{basename(filenames[0])}_{basename(filenames[1])}", "transaction": [] }
        prev_owner_id = None
        nth_car = 0
        i = -1
        for index, row in full_data.iterrows():
            # since "index" is the index of the of the csv file, it is not recommended for use after sorting 
            i += 1
            if prev_owner_id == row["owner_id"]:
                nth_car += 1
                json_res["transaction"][i-nth_car]["vehicles"].append({
                    "id": row["id"],
                    "make": row["make"],
                    "vin_number": row["vin_number"],
                    "model_year": row["model_year"]
                })
            else:
                if nth_car > 0: nth_car = 0
                prev_owner_id = row["owner_id"]
                json_res["transaction"].append({
                    "date": row["date"],
                    "customer": {
                        "id": row["owner_id"],
                        "name": row['name'],
                        "address": row['address'],
                        "phone": row['phone']
                    },
                    "vehicles": [
                        {
                            "id": row["id"],
                            "make": row["make"],
                            "vin_number": row["vin_number"],
                            "model_year": row["model_year"]
                        }
                    ]
                })
        json_data = json.dumps(json_res, indent=3, ensure_ascii=False)
        parser.parse_to_json(json_data)
