import sys
from parser.transaction_processor import process
import pymongo
from decouple import config

filetype = sys.argv[1].lower()
filenames = sys.argv[2:]

process(filenames, filetype)