from pydantic import BaseModel, EmailStr, Field


class LoginUserRequest(BaseModel):
    email: EmailStr = Field(
        ..., title='Email', description='The email of the user'
    )
    password: str = Field(..., min_length=8, max_length=20)
