import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')

print('Connected to database')

# Create a table for the papers
conn.execute('''
    CREATE TABLE papers (
        id VARCHAR(50) PRIMARY KEY,
        submitter VARCHAR(255) NOT NULL,
        authors TEXT NOT NULL,
        title TEXT NOT NULL,
        abstract TEXT NOT NULL,
        update_date DATE
    );
''')

# Create a table for categories
conn.execute('''
    CREATE TABLE categories (
        category_code VARCHAR(50) PRIMARY KEY
    );
''')

# Table for paper-category mapping
conn.execute('''
    CREATE TABLE papers_categories (
        paper_id VARCHAR(50),
        category_code VARCHAR(50),
        PRIMARY KEY (paper_id, category_code),
        FOREIGN KEY (paper_id) REFERENCES papers(id),
        FOREIGN KEY (category_code) REFERENCES categories(category_code)
    );
''')

print("papers/categories/mapping tables created")

conn.close()


