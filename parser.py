from parser.transaction_processor import process
from decouple import config
import argparse

parser = argparse.ArgumentParser(description='Convert XML and CSV files to JSON.')
parser.add_argument('--db', '--database', action='store_true', help='store in the Database')
parser.add_argument('--l', '--locally', action='store_true', help='store locally')
parser.add_argument('filestype', type=str, nargs=1,
                    help='File(s) to be processed')
parser.add_argument('filenames', type=str, nargs='+',
                    help='File to be processed')

args = parser.parse_args()

if not process(args.filenames, args.filestype[0], args.db, args.l):
    print(parser)