import csv
import xml.etree.ElementTree
from posixpath import basename, splitext

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