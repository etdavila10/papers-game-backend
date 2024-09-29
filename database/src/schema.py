import sqlite3

def create_tables(db_name='database.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        # Enable foreign key support (important for maintaining referential integrity)
        cursor.execute("PRAGMA foreign_keys = ON;")

        # create categories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
        """)
        print("Table 'categories' created or already exists.")

        # create papers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS paper_ids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                identifier TEXT UNIQUE NOT NULL
            );
        """)
        print("Table 'paper_ids' created or already exists.")

        # create join table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS category_paper (
                category_id INTEGER NOT NULL,
                paper_id INTEGER NOT NULL,
                PRIMARY KEY (category_id, paper_id),
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
                FOREIGN KEY (paper_id) REFERENCES paper_ids(id) ON DELETE CASCADE
            );
        """)
        print("Table 'category_paper' created or already exists.")

        # create indices for querying
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_paper_identifier ON paper_ids(identifier);
        """)
        print("Index 'idx_paper_identifier' created or already exists.")

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_category_name ON categories(name);
        """)
        print("Index 'idx_category_name' created or already exists.")

        # commit changes
        conn.commit()
        print("All tables and indices have been successfully created.")

    except sqlite3.Error as e:
        print(f"An error occurred while creating tables: {e}")
        # Rollback any changes if an error occurs
        conn.rollback()

    finally:
        # Close the cursor and the connection
        cursor.close()
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    create_tables()
