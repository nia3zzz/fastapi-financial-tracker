from pydantic import BaseModel, EmailStr, Field


# create the user model that will hold data to be recieved from the client and it will also work as a type validator
class UserModel(BaseModel):
    first_name: str = Field(min_length=3, max_length=13)
    last_name: str = Field(min_length=3, max_length=13)
    email: EmailStr
    password: str = Field(mix_length=6, max_length=24)
