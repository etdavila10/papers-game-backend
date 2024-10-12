from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis
import asyncio

from . import arxiv
import json
import sqlite3

app = FastAPI()
redis = None

num_of_articles = 200

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    "https://tranquil-starship-92a3ed.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

"""
    This should be the function that actually loads articles
    into the Redis Cache. That way I can call it from
    multiple locations in the code as a helper function.
"""


async def load_articles(num_articles):

    conn = sqlite3.connect("database/src/database.db")

    cursor = conn.cursor()

    cursor.execute(
        f"SELECT identifier FROM paper_ids ORDER BY RANDOM() LIMIT {num_articles}"
    )

    paper_ids = [row[0] for row in cursor.fetchmany(num_articles)]

    conn.close()

    response_dict = arxiv.call_arxiv_api(paper_ids)

    # List of dictionaries
    articles_list = response_dict["feed"]["entry"]

    # Add data to redis cache
    for id, article in zip(paper_ids, articles_list):
        await redis.set(id, json.dumps(article))


async def check_sufficient_articles():
    while True:
        num_keys = await redis.dbsize()
        if num_keys < (num_of_articles // 2):
            articles_fill = num_of_articles - num_keys
            await load_articles(articles_fill)
            print(f"{articles_fill} articles were added")

        await asyncio.sleep(30)


"""
    Want to set up redis cache so that articles
    can be retrieved instantly from requests
"""


@app.on_event("startup")
async def startup_event():

    global redis
    redis = Redis(host="localhost", port=6379, decode_responses=True)

    asyncio.create_task(check_sufficient_articles())


@app.on_event("shutdown")
async def shutdown_event():
    await redis.close()

@app.get("/random")
async def read_articles():
    random_key = await redis.randomkey()
    cached_data = await redis.get(random_key)
    # remove this from the article pool
    await redis.delete(random_key)

    # Get a second article
    random_key_2 = await redis.randomkey()
    cached_data_2 = await redis.get(random_key_2)
    await redis.delete(random_key_2)

    print(f"The article with id {random_key} was removed")
    print(f"The article with id {random_key_2} was removed")

    if cached_data and cached_data_2:
        return [json.loads(article) for article in [cached_data, cached_data_2]]
    else:
        return {"error": "Item not found"}
