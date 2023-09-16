import random
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr
import requests
import socket

# Configuration settings
class Config:
    MONGO_HOST = "mongohost"
    MONGO_PORT = 27017
    MONGO_DB = "covid_tweets"
    MONGO_COLLECTION = "merged_data"
    INPUT_HOST = "simulator"
    INPUT_PORT = 5555

# MongoDB connection
class MongoDB:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_HOST, Config.MONGO_PORT)
        self.db = self.client[Config.MONGO_DB]

    def insert_data(self, data):
        self.db[Config.MONGO_COLLECTION].insert_one(data)

# Input source (Socket)
class SocketInput:
    def __init__(self):
        self.socket = None

    def connect(self):
        self.socket = socket.socket()
        self.socket.bind(("0.0.0.0", Config.INPUT_PORT))
        self.socket.listen(4)
        print('Socket is ready')

    def receive_data(self):
        c_socket, addr = self.socket.accept()
        print("Received request from: " + str(addr))
        return c_socket

# Twitter data scraper
class TwitterScraper:
    @staticmethod
    def fetch_covid_data():
        page = requests.get("https://www.worldometers.info/coronavirus/")
        page_content = page.content
        total_cases = BeautifulSoup(page_content, "html.parser").find("div", {"id": "maincounter-wrap"}).text.strip().replace(",", "")
        return total_cases

# Data processing
class DataProcessor:
    def __init__(self, mongo_db):
        self.mongo_db = mongo_db

    def clean_data(self, input_df):
        return input_df.withColumn("value", expr("regexp_replace(value, '#|RT:', '')"))

    def process_stream(self, batch_df, batch_id):
        # Fetch COVID-19 data
        total_cases = TwitterScraper.fetch_covid_data()

        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create merged data
        cleaned_df = self.clean_data(batch_df)
        merged_data = {
            "content": cleaned_df.select("value").rdd.flatMap(lambda x: x).collect(),
            "timestamp": timestamp,
            "total_case_count": total_cases
        }

        # Store merged data in MongoDB
        self.mongo_db.insert_data(merged_data)

if __name__ == "__main__":
    # Create a Spark session
    spark = SparkSession.builder.appName("TwitterCovidDataEngineering").getOrCreate()

    # Initialize input source (Socket) and MongoDB
    socket_input = SocketInput()
    socket_input.connect()
    mongo_db = MongoDB()

    # Initialize data processor
    data_processor = DataProcessor(mongo_db)

    # Start Spark Structured Streaming context with a 20-second batch interval
    stream_query = (
        spark.readStream.format("socket")
        .option("host", Config.INPUT_HOST)
        .option("port", Config.INPUT_PORT)
        .load()
        .writeStream
        .foreachBatch(data_processor.process_stream)
        .trigger(processingTime="20 seconds")  # Set the batch interval to 20 seconds
        .start()
    )

    # Wait for the streaming query to terminate
    stream_query.awaitTermination()
