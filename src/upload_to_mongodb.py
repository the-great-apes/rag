import json
import logging
import os
from collections import defaultdict
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import logging
from .helpers import Summary, list_json_files
import yaml


cfg = yaml.safe_load(open("params.yaml"))
use_openai = cfg["use_openai"]
print(f"use_openai: {use_openai}")

if use_openai:
    COLLECTION_NAME = "openai"
else:
    COLLECTION_NAME = "groq"


def write_document(ref_key, data):
    try:
        mdb_conf = cfg['database']['mongodb']
        client = MongoClient(f"mongodb://{mdb_conf['host']}:{mdb_conf['port']}")
        db = client[mdb_conf['db_name']]  # Replace with your data database name
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
                logging.info(f"New document inserted with ID: {result.upserted_id} into {COLLECTION_NAME} collection")
            else:
                logging.info(f"Existing document updated with key reference: {ref_key} in collection {COLLECTION_NAME}")
        
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

def write_companies(data):
    write_document("companies", {"companies": list(data.keys())})

def write_years(data, comp: str):
    write_document(f"{comp}-years", {"years": list(data[comp].keys())})

def write_report(data, comp: str, year: int):
    write_document(f"{comp}-{year}", {"report": data[comp][year].model_dump_json()})

def main():
    data = defaultdict(defaultdict)

    json_files = list_json_files("/app/data/summary")

    for s in [Summary.load(f) for f in json_files]:
        data[s.company][s.year] = s

    write_companies(data)
    
    companies = list(data.keys())  # Create a static list of keys
    for c in companies:
        write_years(data, c)
        years = list(data[c].keys())  # Create a static list of keys for each company
        for y in years:
            write_report(data, c, y)
    

        
if __name__ == "__main__":
    main()