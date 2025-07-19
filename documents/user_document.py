from pydantic import BaseModel, EmailStr, Field


# create the user model that will hold data to be recieved from the client and it will also work as a type validator
class UserModel(BaseModel):
    first_name: str = Field(min_length=3, max_length=13)
    last_name: str = Field(min_length=3, max_length=13)
    email: EmailStr
    password: str = Field(min_length=6, max_length=24)


# build up class models for the type of user relate routes
class LoginUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=24)


class UpdateUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=24)
    jwt_token: str = Field(max_length=300)
