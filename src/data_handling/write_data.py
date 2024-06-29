from pymongo import MongoClient
from pymongo.errors import PyMongoError
import logging

DATA_DB='mongodb://mongodb-data:27017/'
DB_NAME='data_db'
COLLECTION_NAME='swisshacks'

def write_document(company_ref, data):
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
            filter = {'reference': company_ref}

            # Specify the update operation using MongoDB's $set operator
            update = {'$set': data}

            # Perform the upsert operation
            result = collection.update_one(filter, update, upsert=True)

            # Print feedback on whether a new document was inserted or an existing one updated
            if result.upserted_id:
                logging.info(f"New document inserted with ID: {result.upserted_id}")
            else:
                logging.info(f"Existing document updated with key reference: {company_ref}")
        
        except PyMongoError as e:
            logging.error(f"Error occurred while upserting data: {e}")
    except Exception as e:
        logging.info(f"Failed to connect to MongoDB: {e}")
        return

    finally:
        if 'client' in locals():
            client.close()  # Always close the client connection at the end
