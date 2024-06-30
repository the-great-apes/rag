import json
import logging
import os
from collections import defaultdict
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import logging
from .helpers import Summary, list_json_files

DATA_DB='mongodb://mongodb-data:27017/'
DB_NAME='data_db'
COLLECTION_NAME='swisshacks'

def write_document(ref_key, data):
    try:
        client = MongoClient(DATA_DB)
        db = client[DB_NAME]  # Replace with your data database name
        collection_names = db.list_collection_names()
        if not COLLECTION_NAME in collection_names:
            db.create_collection(COLLECTION_NAME)
        collection = db[COLLECTION_NAME]  
        
        # Check if the connection is successful
        client.server_info()  # This will raise an exception if the connection fails
        
        logging.info("Successfully connected to MongoDB.")

        try:
            filter = {'reference': ref_key}

            # Specify the update operation using MongoDB's $set operator
            update = {'$set': data}

            # Perform the upsert operation
            result = collection.update_one(filter, update, upsert=True)

            # Print feedback on whether a new document was inserted or an existing one updated
            if result.upserted_id:
                logging.info(f"New document inserted with ID: {result.upserted_id}")
            else:
                logging.info(f"Existing document updated with key reference: {ref_key}")
        
        except PyMongoError as e:
            logging.error(f"Error occurred while upserting data: {e}")
    except Exception as e:
        logging.info(f"Failed to connect to MongoDB: {e}")
        return

    finally:
        if 'client' in locals():
            client.close()  # Always close the client connection at the end


try:
    log_level = os.environ['LOG_LEVEL'].upper()
except KeyError:
    log_level = 'INFO'

log_level_mapping = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

logging.basicConfig(level=log_level_mapping.get(log_level, logging.WARNING))

DATA_PATH = "/app/data"
# Print the parsed data

COMPANY_REFS = ["ABB", "IBM", "PostFinance", "Raiffeisen", "Siemens", "UBS"]


def write_companies():
    write_document("companies", {"companies": list(data.keys())})

def write_years(comp: str):
    write_document(f"{comp}-years", {"years": list(data[comp].keys())})

def write_report(comp: str, year: str):
    write_document(f"{comp}-{year}", {"report": data[comp][int(year)].model_dump_json()})


def main():
    data = defaultdict(defaultdict)

    json_files = list_json_files(Path("data/summary"))

    for s in [Summary.load(f) for f in json_files]:
        data[s.company][s.year] = s

    write_companies()
    for c in data.keys():
        write_years(c)
        for y in data['c'].keys():
            write_report(c, y)
    

        
if __name__ == "__main__":
    main()