import sys
from parser.utils import without_keys
from decouple import config
import pymongo
import json

DB_NAME = config('DB_NAME')
DB_USERNAME = config('DB_USERNAME')
DB_PASSWORD = config('DB_PASSWORD')

command = sys.argv[1].lower()
db_args = sys.argv[2:]

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient[DB_NAME]

if command == 'add-user':
    mydb.command("createUser", DB_USERNAME, pwd=DB_PASSWORD, roles=[{'role':'readWrite','db':DB_NAME}], mechanisms=["SCRAM-SHA-1"])
elif command == 'drop-user':
    mydb.command("dropUser", DB_USERNAME)
elif command == 'drop-db':
    mydb.command("dropDatabase")
elif command == 'list':
    mycol = mydb[db_args[0]]
    for x in mycol.find():
        print(x['_id'], json.dumps(without_keys(x, {"_id"}), indent=3, ensure_ascii=False))
    