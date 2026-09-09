import psycopg
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

query = 'database'
query_embedding = model.encode(query)

with psycopg.connect('dbname=sementic_search user=arpit') as conn:
    register_vector(conn)
    with conn.cursor() as cursor:
        cursor.execute("""
                    SELECT id, content, embedding <=> %s AS distance FROM documents
                    WHERE embedding IS NOT NULL
                    ORDER BY embedding<=>%s;""", (query_embedding, query_embedding))
        res = cursor.fetchall()

for row in res:
    print(row)
