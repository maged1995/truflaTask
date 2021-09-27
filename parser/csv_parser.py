from posixpath import basename, splitext
from .parser_main import ParserMain
import pandas as pd
import requests
import json

class CSVParser(ParserMain):
    def __init__(self, file_name, file_name2):
        ParserMain.__init__(self, file_name)
        self.file_name2 = file_name2

    def pre_process(self):
        data1 = pd.read_csv(self.file_name)
        data2 = pd.read_csv(self.file_name2)

        if not 'owner_id' in data1.keys():
            data1['owner_id'] = data1.pop('id')
        else:
            data2['owner_id'] = data2.pop('id')
            
        full_data = pd.merge(data1, data2 ,on='owner_id').sort_values(by=['owner_id'])
        json_res = { "file_name": f"{basename(self.file_name)}_{basename(self.file_name2)}", "transaction": [] }
        prev_owner_id = None
        nth_car = 0
        i = -1
        for index, row in full_data.iterrows():
            # since "index" is the index of the records in the csv file, it is not recommended for use after sorting
            i += 1

            vin = row["vin_number"]
            model_year = row["model_year"]
            response = requests.get(f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json&modelyear={model_year}")
            extra_info = response.json()['Results'][0]
            
            if prev_owner_id == row["owner_id"]:
                nth_car += 1
                json_res["transaction"][i-nth_car]["vehicles"].append({
                    "id": row["id"],
                    "make": row["make"],
                    "vin_number": row["vin_number"],
                    "model_year": row["model_year"],
                    "model": extra_info['Model'],
                    "manufacturer": extra_info['Manufacturer'],
                    "plant_country": extra_info['PlantCountry'],
                    "vehicle_type": extra_info['VehicleType']
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
                            "model_year": row["model_year"],
                            "model": extra_info['Model'],
                            "manufacturer": extra_info['Manufacturer'],
                            "plant_country": extra_info['PlantCountry'],
                            "vehicle_type": extra_info['VehicleType']
                        }
                    ]
                })
        self.json_data = json.dumps(json_res, indent=3, ensure_ascii=False)
        return json_res

    def parse_to_json(self):
        new_file_name = splitext(basename(self.file_name))[0] + '.json'
        with open(f"output/csv/{self.time_stamp}_{new_file_name}", "w") as json_file:
            json_file.write(self.json_data)
            json_file.close()