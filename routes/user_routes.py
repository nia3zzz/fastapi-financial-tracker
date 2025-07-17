from fastapi import APIRouter
from documents.user_document import UserModel, LoginUser
from utils.connectMongoDB import mongodb
from fastapi import HTTPException
import bcrypt
import os
import jwt

user_router = APIRouter()

# get hold of the jwt obect in the .env file
key = os.getenv("JWT_SECRET")

if not key:
    raise ValueError("No JWT_SECRET found in .env file.")


# route for creating a new user
@user_router.post("/users/")
async def create_users(request_body: UserModel):
    # check if no user already exists with the provided email
    if mongodb.user.find_one({"email": request_body.email}) is not None:
        raise HTTPException(
            status_code=409,
            detail={
                "status": "error",
                "message": "User with this email already exists.",
            },
        )

    # hash the provided user password
    hashedPassword = bcrypt.hashpw(
        request_body.password.encode("utf-8"), bcrypt.gensalt(10)
    )

    try:
        # inset the password into db
        mongodb.user.insert_one(
            {
                "first_Name": request_body.first_name,
                "last_name": request_body.last_name,
                "email": request_body.email,
                "password": hashedPassword,
            }
        )

        return {"status": "success", "message": "User has been created successfully."}
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={"status": "error", "message": "Something went wrong."},
        )


# route for the user login route
@user_router.post("/users/login/")
def login_user(request_body: LoginUser):
    # check if a user exists with the provided email in the request body
    found_user = mongodb.user.find_one({"email": request_body.email})

    if found_user is None:
        raise HTTPException(
            status_code=409,
            detail={
                "status": "error",
                "message": "Invalid credential.",
            },
        )

    print(found_user)

    # compare the passwords to check if they are matching with the user document's hashed password
    if (
        bcrypt.checkpw(request_body.password.encode("utf-8"), found_user["password"])
        == False
    ):
        raise HTTPException(
            status_code=409,
            detail={
                "status": "error",
                "message": "Invalid credential.",
            },
        )

    try:
        # create a jwt using the user id and return it to the user
        encoded_jwt = jwt.encode({"user_id": "payload"}, key, algorithm="HS256")

        # return the jwt to the client
        return {
            "status": "success",
            "message": "User logged in successfully.",
            "encoded_jwt": encoded_jwt,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"status": "error", "message": "Something went wrong."},
        )
