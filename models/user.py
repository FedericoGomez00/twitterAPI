# Python
from datetime import date
from typing import Optional
from uuid import UUID
from bson import ObjectId

# Pydantic
from pydantic import BaseModel, EmailStr, Field


# User models

class UserBase(BaseModel):
    _id: str = Field(...)
    email: EmailStr = Field(...)


class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[date] = Field(default=None)

class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )