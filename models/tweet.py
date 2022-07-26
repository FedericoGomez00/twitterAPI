from models.user import User

# Python
from datetime import datetime
from typing import Optional
from uuid import UUID
from bson import ObjectId

# Pydantic
from pydantic import BaseModel, Field


# Tweet model

class Tweet(BaseModel):
    _id: str = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)
