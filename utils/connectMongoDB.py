from pymongo import MongoClient
import os

# function for connecting to the mongodb database using the uri


def connectMongoDB():
    # check if the environmental variables has been provided in .env file
    if not os.getenv("MONGODBURI"):
        raise ValueError("No MONGODBURI found in .env file.")
    try:
        client = MongoClient(os.getenv("MONGODBURI"))
        print(
            f"Connected to database host: {client.address}",
        )
    except Exception as e:
        raise SystemError(
            f"Error connecting to mongodb, {e}",
        )
