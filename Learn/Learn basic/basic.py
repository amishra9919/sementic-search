import psycopg

""" 
Created a db already (what? CREATED A DB) in PostgreSQL with name 'sementic_search'.
So, sementic_search=# what ? it is a db

How it is created ? (below)

CREATE DATABASE sementic_search;

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
    user="postgres",
    password="arpitm11814"
)
# conn = psycopg.connect(
#     "dbname=semantic_search user=arpit"
# )

#here 'conn' represents the connection Session (channel btwn python and postgres servr)

cursor = conn.cursor() # Cursor as the object use to execute SQL and retrieve results 
                       # It actually send SQL commands .. [execute SQL and retrieve results means = obj can exec func]


"""
Create a TABLE in PostgreSQL with name 'documents'

CREATE TABLE documents (
id SERIAL PRIMARY KEY,
content TEXT
);

- id(col name) : Every document needs an identifier.
  SERIAL (as datatype) tells PostgreSQL to automatically generate numbers: 1,2,3....
  PRIMARY KEY = id uniquely identifies each row.

- content (col name) : This is where the actual document/chunk text will eventually live.
  TEXT content will be in TEXT datatype
"""

# cursor.execute("INSERT INTO documents(content) VALUES('Hi this is Arpit');")
cursor.execute("SELECT id, content FROM documents;")

# result = cursor.fetchone() # takes the first row returned by PostgreSQL.

result = cursor.fetchall()

print('result', result)

cursor.close() #for small scripts like this .close() dosnt matter but for long-run app'n it matters
conn.close()

#==========================================================================================================================

# Real applications commonly use Python's with context manager so resources are cleaned up automatically

with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="sementic_search",
    user="arpit",
    password="arpitm11814"
) as conn :
    with conn.cursor() as cursor:
        print("Connected")
        cursor.execute("SELECT id, content FROM documents;")
        result = cursor.fetchall()
        print("result: ", result)

#==========================================================================================================================

##Creating Embedding 
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
text = 'PostgreSQL is a relational database system.'

embedding = model.encode(text)

print("Embedding: ", type(embedding))
