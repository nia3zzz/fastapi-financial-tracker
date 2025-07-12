from fastapi import FastAPI
from dotenv import load_dotenv
from utils.connectMongoDB import connectMongoDB

# load the environmental variables
load_dotenv()

# connect to the mongodb database specified in the .env file
connectMongoDB()

# initialize the app and run it
app = FastAPI()


# root page that return a message
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI + uv!"}
