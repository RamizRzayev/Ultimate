# Ultimate
# Twitter COVID Data Engineering

This project collects and processes Twitter data related to COVID-19 using Spark Streaming and stores it in a MongoDB database. It consists of the following components:

- 'simulator.py`: Simulates incoming Twitter data and sends it to a specified host and port.
- 'processor.py`: Processes the incoming Twitter data using Spark Streaming and stores it in MongoDB.
- 'Dockerfile`: Contains instructions for building a Docker image for this project.
- 'docker-compose.yml`: Defines the Docker services and containers required to run the project.
- 'check_Mongo_collection.py`: A script to check the MongoDB collection to ensure data is being properly stored.

## Prerequisites

Before running this project, ensure you have the following prerequisites installed:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started .   Configuration :You can customize the configuration settings in the Config class in simulator.py and processor.py to suit your needs. 	


1. **Download the Project**

   Clone this repository to your local machine:

   git clone https://github.com/RamizRzayev/Ultimate
   
2. **Navigate to the folder**    
   
   cd twitter-covid-data-engineering

3. **Build and start containers** 
    
   docker-compose up --build -d

 	
4. **Check a result** 
    A minutes later check 
	
   python check_Mongo_collection.py