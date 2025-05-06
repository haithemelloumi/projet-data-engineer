import os
import sqlite3

DB_PATH = '/data/sales.db'
schema_file = "schema.sql"

# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Drop existing tables if they exist
cursor.execute("DROP TABLE IF EXISTS ventes")
cursor.execute("DROP TABLE IF EXISTS produits")
cursor.execute("DROP TABLE IF EXISTS magasins")

# Load and execute schema
with open(schema_file, "r", encoding="utf-8") as f:
    schema = f.read()
    cursor.executescript(schema)

conn.commit()
conn.close()
print(f"✅ Database created with success")