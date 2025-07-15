from fastapi import FastAPI
from dotenv import load_dotenv
from routes.user_routes import user_router

# load the environmental variables
load_dotenv()

# initialize the app and run it
app = FastAPI()

# import the router from the user routes
app.include_router(user_router)


# root page that return a message
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI + uv!"}
