from posixpath import basename, splitext
from .parser_main import ParserMain
from .utils import without_keys, assert_xml_format, keys_snake
import xmltodict
import json
import requests

class XMLParser(ParserMain):
    def __init__(self, file_name):
        ParserMain.__init__(self, file_name)
        if not assert_xml_format(file_name):
            self.errors.add(f"{file_name} is not supported, either fix it or submit another file")

    def enrich_data(self):
        i=-1
        for cd in self.customer_data["units"]["auto"]["vehicle"]:
            i+=1
            vin = cd["vin_number"]
            model_year = cd["model_year"]

            try:
                response = requests.get(f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json&modelyear={model_year}")
                extra_info = response.json()['Results'][0]
                if response.status_code == 200:
                    self.customer_data["units"]["auto"]["vehicle"][i].update({
                        "model": extra_info['Model'],
                        "manufacturer": extra_info['Manufacturer'],
                        "plant_country": extra_info['PlantCountry'],
                        "vehicle_type": extra_info['VehicleType']
                    })
                else:
                    self.exceptions.append("wrong or unavailable vehicle data")
            except requests.exceptions.ConnectionError:
                self.exceptions.add('No Internet Connection for Data enrichment')
            except:
                self.exceptions.add('Unknown Error Occurred. Contact the developer')

    def pre_process(self):
        with open(self.file_name, mode='r') as xml_file:
            data_dict = xmltodict.parse(xml_file.read(), encoding='utf-8')
            xml_file.close()
            data_dict = keys_snake(data_dict)
            self.customer_data = data_dict["insurance"]["transaction"]["customer"]
            customer_exclude_data = {"units"}
            
            self.enrich_data()

            json_res = {
                "file_name": basename(self.file_name),
                "transaction": [
                    {
                        "date": data_dict["insurance"]["transaction"]["date"],
                        "customer": without_keys(self.customer_data, customer_exclude_data),
                        "vehicles": self.customer_data["units"]["auto"]["vehicle"]
                    }
                ]
            }
            self.json_data = json.dumps(json_res, indent=3, ensure_ascii=False).replace("@", "")
            if self.exceptions: print(self.exceptions)
            return json_res

    def parse_to_json(self):
            new_file_name = splitext(basename(self.file_name))[0] + '.json'
            with open(f"output/xml/{self.time_stamp}_{new_file_name}", "w", encoding='utf-8') as json_file:
                json_file.write(self.json_data)
                json_file.close()