import psycopg

""" 
Created a db already in PostgreSQL with name 'sementic_search'

CREATE DATABASE semantic_search;

    Python program
        │
        │ psycopg
        ▼
    PostgreSQL server
"""
conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="sementic_search",
    user="arpit"
)
# conn = psycopg.connect(
#     "dbname=semantic_search user=arpit"
# )

cursor = conn.cursor() # Think of the cursor as the object use to execute SQL and retrieve results.


"""
Created a TABLE already in PostgreSQL with name 'documents'

CREATE TABLE documents (
id SERIAL PRIMARY KEY,
content TEXT
);

- id : Every document needs an identifier.
   - SERIAL tells PostgreSQL to automatically generate numbers: 1,2,3....
   - PRIMARY KEY = id uniquely identifies each row.

- content TEXT : This is where the actual document/chunk text will eventually live.
"""

cursor.execute("SELECT id, content FROM documents;")

# result = cursor.fetchone() # takes the first row returned by PostgreSQL.

result = cursor.fetchall()

print(result)

cursor.close()

conn.close()