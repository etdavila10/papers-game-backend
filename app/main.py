from fastapi import FastAPI

from . import arxiv
import json
import sqlite3

app = FastAPI()

@app.get("/")
def read_root():
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
