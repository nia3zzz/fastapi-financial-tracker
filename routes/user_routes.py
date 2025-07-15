from fastapi import APIRouter
from documents.user_document import UserModel
from utils.connectMongoDB import mongodb
from fastapi import HTTPException
import bcrypt

user_router = APIRouter()


# route for creating a new user
@user_router.post("/users/")
async def read_users(request_body: UserModel):
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
