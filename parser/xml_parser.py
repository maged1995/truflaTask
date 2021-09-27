from posixpath import basename, splitext
from .parser_main import ParserMain
from .utils import without_keys
import xmltodict
import json
import requests

class XMLParser(ParserMain):
    def enrich_data(self):
        self.customer_data
        vin = self.customer_data["Units"]["Auto"]["Vehicle"][0]["VinNumber"]
        model_year = self.customer_data["Units"]["Auto"]["Vehicle"][0]["ModelYear"]
        response = requests.get(f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json&modelyear={model_year}")
        extra_info = response.json()['Results'][0]

        if response.status_code == 200:
            self.customer_data["Units"]["Auto"]["Vehicle"][0].update({
                "model": extra_info['Model'],
                "manufacturer": extra_info['Manufacturer'],
                "plant_country": extra_info['PlantCountry'],
                "vehicle_type": extra_info['VehicleType']
            })

    def pre_process(self):
        with open(self.file_name, mode='r') as xml_file:
            data_dict = xmltodict.parse(xml_file.read(), encoding='utf-8')
            xml_file.close()
            self.customer_data = data_dict["Insurance"]["Transaction"]["Customer"]
            customer_exclude_data = {"Units"}
            
            self.enrich_data()

            json_res = {
                "file_name": basename(self.file_name),
                "transaction": [
                    {
                        "date": data_dict["Insurance"]["Transaction"]["Date"],
                        "customer": without_keys(self.customer_data, customer_exclude_data),
                        "Vehicles": self.customer_data["Units"]["Auto"]["Vehicle"]
                    }
                ]
            }
            self.json_data = json.dumps(json_res, indent=3, ensure_ascii=False).replace("@", "")
            return json_res

    def parse_to_json(self):
            new_file_name = splitext(basename(self.file_name))[0] + '.json'
            with open(f"output/xml/{self.time_stamp}_{new_file_name}", "w", encoding='utf-8') as json_file:
                json_file.write(self.json_data)
                json_file.close()