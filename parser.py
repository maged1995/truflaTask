import sys
from parser.transaction_processor import pre_process

filetype = sys.argv[1].lower()
filenames = sys.argv[2:]

p = pre_process(filenames, filetype)