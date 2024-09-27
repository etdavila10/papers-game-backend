import json
import sqlite3

# Sample JSON data (as provided)
# ToDo: Replace this with the actual JSON data
with open('data/remapped_data.json', 'r') as f:
    json_data = json.load(f)

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Enable foreign key support
cursor.execute("PRAGMA foreign_keys = ON;")

# Insert categories and paper_ids
category_id_map = {}
paper_id_map = {}

# Insert categories
for category in json_data:
    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?);", (category,))
    cursor.execute("SELECT id FROM categories WHERE name = ?;", (category,))
    category_id = cursor.fetchone()[0]
    category_id_map[category] = category_id

# Insert paper_ids
all_papers = set()
for papers in json_data.values():
    all_papers.update(papers)

for paper in all_papers:
    cursor.execute("INSERT OR IGNORE INTO paper_ids (identifier) VALUES (?);", (paper,))
    cursor.execute("SELECT id FROM paper_ids WHERE identifier = ?;", (paper,))
    paper_id = cursor.fetchone()[0]
    paper_id_map[paper] = paper_id

# Populate the join table
for category, papers in json_data.items():
    category_id = category_id_map[category]
    for paper in papers:
        paper_id = paper_id_map[paper]
        cursor.execute("""
            INSERT OR IGNORE INTO category_paper (category_id, paper_id)
            VALUES (?, ?);
        """, (category_id, paper_id))

# Commit changes and close the connection
conn.commit()
conn.close()

print('everything is done')