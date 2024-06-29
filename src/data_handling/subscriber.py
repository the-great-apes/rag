from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.json_util import dumps
import logging
PUB_SUB_DB='mongodb://mongodb-pubsub:27017/'

def subscribe_to_messages():
    try:
        # Connect to MongoDB
        client = MongoClient(PUB_SUB_DB)
        db = client['pubsub_db']  # Replace with your pub-sub database name
        collection = db['messages']  # Replace with your collection name where messages are stored

        # Watch the collection for changes (insertions)
        pipeline = [{'$match': {'operationType': 'insert'}}]
        with collection.watch(pipeline) as stream:
            print("Started listening for new messages...")
            for change in stream:
                # Process each change event (insertion)
                if change.get('fullDocument'):
                    message = change['fullDocument']
                    print(f"Received new message: {dumps(message)}")
                    #TODO: handle with RAG LLM
    
    except PyMongoError as e:
        logging.error(f"Error occurred: {e}")
        # Handle error (retry, logging, etc.)
