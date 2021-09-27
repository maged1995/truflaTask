# Trufla Code Challenge – Python Developer

## General installation Notes

1. Install Python 3
2. These Python packages should exist while using this project. if not, install them using pip (ex: `pip install <package_name>`):
   - argparse
   - posixpath
   - pandas
   - requests
   - csv
   - xml
   - json
   - decouple
   - pymongo
   - xmltodict
3. Install MongoDB by following [these instructions](https://docs.mongodb.com/manual/installation/)
   --At this point the project should be usable--
4. Add a new file named `.env`, this is where the environment variables should be. there already is a sample for the `.env` file named `.env.sample`

---

the database creations and usage work according to the environment variables

## Database commands:

1. New DB User filled by the environment Variables: `python3 db.py add-user`
2. Removing the DB User filled by the environment variables: `python3 db.py drop-user`
3. Dropping the DB filled by the environment variables: `python3 db.py drop-user`
4. list all items in the collection (csv or xml): `python3 db.py drop-user <collection_name>`

---

## Parser Examples:

1. parsing xml file: `python3 parser.py xml path/to/file.xml`
2. parsing CSV files: `python3 parser.py csv path/to/file1.xml path/to/file2.csv`
3. parsing the file(s) to local output: `python3 parser.py <file_type> <file_paths> --l`
4. parsing the file(s) to Database: `python3 parser.py <file_type> <file_paths> --db`
5. parsing the file(s) to both local output and Database: `python3 parser.py <file_type> <file_paths> --l --db`
