import csv

def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}

def assert_csv_format(file_name):
    with open(file_name, newline = "") as csvfile:
        try:
            csv.Sniffer().sniff(csvfile.read(1024), delimiters = ",")
            return True
        except:
            return False