import pymongo

# MongoDB connection settings
mongo_host = "localhost"  # Replace with your MongoDB host
mongo_port = 27017        # Replace with your MongoDB port
mongo_db = "covid_tweets" # Replace with your MongoDB database name
mongo_collection = "merged_data"  # Replace with your MongoDB collection name

# Connect to MongoDB
client = pymongo.MongoClient(mongo_host, mongo_port)
db = client[mongo_db]
collection = db[mongo_collection]

# Query and print documents in the collection
documents = collection.find()
for document in documents:
    print(document)

# Close the MongoDB connection
client.close()
