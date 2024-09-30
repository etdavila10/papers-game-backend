from fastapi import FastAPI, Depends, HTTPException

from . import arxiv
import json
import sqlite3

app = FastAPI()

API_KEY = "test123"

def validate_api_key(api_key: str):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")

@app.get("/")
def read_root(api_key: str = Depends(validate_api_key)):
    return {"Hello": "World"}

@app.get("/random")
def read_articles(api_key: str = Depends(validate_api_key)):
    conn = sqlite3.connect('database/src/database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT identifier FROM paper_ids ORDER BY RANDOM() LIMIT 2')

    paper_ids = [row[0] for row in cursor.fetchmany(2)]

    conn.close()

    response_dict = arxiv.call_arxiv_api(paper_ids)

    # List of dictionaries
    articles_list = response_dict["feed"]["entry"]

    return articles_list
