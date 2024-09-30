from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import arxiv
import json
import sqlite3

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://tranquil-starship-92a3ed.netlify.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"]
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/random")
def read_articles():
    conn = sqlite3.connect('database/src/database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT identifier FROM paper_ids ORDER BY RANDOM() LIMIT 2')

    paper_ids = [row[0] for row in cursor.fetchmany(2)]

    conn.close()

    response_dict = arxiv.call_arxiv_api(paper_ids)

    # List of dictionaries
    articles_list = response_dict["feed"]["entry"]

    return articles_list
