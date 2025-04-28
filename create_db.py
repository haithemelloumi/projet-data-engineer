import os
import sqlite3

# Path of SQLite database
db_path = os.getenv("DB_PATH", "sales.db")
schema_file = "schema.sql"

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Load SQL file
with open(schema_file, "r", encoding="utf-8") as f:
    schema_sql = f.read()

# Execute SQL queries 
cursor.executescript(schema_sql)

# Save and close
conn.commit()
conn.close()

print(f"✅ Database created with success at : {db_path}")