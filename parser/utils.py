import csv
import xml.etree.ElementTree
from posixpath import basename, splitext
import re

def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}

def assert_csv_format(file_name):
    if splitext(basename(file_name))[1] == '.csv':
        with open(file_name, newline = "") as csvfile:
            try:
                csv.Sniffer().sniff(csvfile.read(1024), delimiters = ",")
                return True
            except:
                return False
    else:
        return False

def assert_xml_format(file_name):
    print(splitext(basename(file_name))[1])
    if splitext(basename(file_name))[1] == '.xml':
        try:
            xml.etree.ElementTree.parse(file_name)
            return True
        except:
            return False
    else:
        return False


def camel_to_snake(str):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', str).lower().replace("@", "")

def keys_snake(test_dict):
    res = dict()
    for key in test_dict.keys():
        if isinstance(test_dict[key], dict):
            res[camel_to_snake(key)] = keys_snake(test_dict[key])
        elif isinstance(test_dict[key], list):
            res[camel_to_snake(key)] = []
            for t in test_dict[key]:
                res[camel_to_snake(key)].append(keys_snake(t))
        else:
            res[camel_to_snake(key)] = test_dict[key]
    return res