# Models
from models.user import User, UserRegister
from models.tweet import Tweet

# Python
import asyncio
import json
from typing import List
from uuid import UUID
from bson.objectid import ObjectId


# FastAPI
from fastapi import FastAPI, Path, Query, Body, status
from fastapi.encoders import jsonable_encoder

# Pymongo
# from pymongo import MongoClient
import motor.motor_asyncio

# Uvicorn server
import uvicorn

app = FastAPI()

MONGO_DETAILS = 'mongodb://localhost:27017'
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

db = client.twitter_db
users = db.get_collection("users")
tweets = db.tweets


# Path operations

@app.get(
    path="/"
)
def home():
    return {"Twitter API": "Working!"}

## Users

### Register a user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a user",
    tags=["Users"]
)
async def signup(user: UserRegister = Body(...)):
    """
    Signup

    This path operation register a user in the app

    Parameters: 
        - Request body parameter
            - user: UserRegister
    
    Returns a json with the basic user information: 
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    
    user = jsonable_encoder(user)

    new_user = await users.insert_one(user)
    return await users.find_one({'_id':new_user.inserted_id})
    

### Login a user
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    tags=["Users"]
)
def login():
    pass

### Show all users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
async def show_all_users():
    """
    This path operation shows all users in the app

    Parameters: 
        -

    Returns a json list with all users in the app, with the following keys: 
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    return await users.find().to_list(1000)

### Show a user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["Users"]
)
async def show_a_user(
    user_id: str = Path(...)
):
    """
    This path operation shows a users with the user ID

    Parameters: 
        - user_id: UUID

    Returns a json with a users, with the following keys: 
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    return await users.find_one({'_id': ObjectId(user_id)})

### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"]
)
async def delete_a_user(
    user_id: str = Path(...)
):
    user_return = await users.find_one({'_id': ObjectId(user_id)})
    await users.delete_one({'_id': ObjectId(user_id)})
    return user_return

### Update a user
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=["Users"]
)
def update_a_user():
    pass


## Tweets

### Show all tweets (home)
@app.get(
    path="/tweets",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweet"]
)
async def show_all_tweets():
    return await tweets.find().to_list(1000)

### Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweet"]
)
async def show_a_tweet(
    tweet_id: str = Path(...)
):
    return await tweets.find_one({'_id': ObjectId(tweet_id)})

### Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Publish a tweets",
    tags=["Tweet"]
)
async def post_tweet(tweet: Tweet = Body(...)):
    """
    Post a Tweet

    This path operation post a tweet in the app

    Parameters: 
        - Request body parameter
            - tweet: Tweet
    
    Returns a json with the basic tweet information: 
        tweet_id: UUID  
        content: str    
        created_at: datetime
        updated_at: Optional[datetime]
        by: User
    """
    tweet = jsonable_encoder(tweet)
    new_tweet = await tweets.insert_one(tweet)
    return await tweets.find_one({'_id': new_tweet.inserted_id})

### Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Update a tweets",
    tags=["Tweet"]
)
def update_tweet():
    pass

### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweets",
    tags=["Tweet"]
)
async def delete_tweet(
    tweet_id: str = Path(...)
):
    tweet_return = await tweets.find_one({'_id': ObjectId(tweet_id)})
    await tweets.delete_one({'_id': ObjectId(tweet_id)})
    return tweet_return


# Entry point
if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)