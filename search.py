import psycopg
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

query = "computer learning from examples"
query_embedding = model.encode(query)

with psycopg.connect('dbname=sementic_search user=arpit') as conn:
    register_vector(conn)
    with conn.cursor() as cursor:
         #If you don't care about seeing the distance value, you can completely remove it from SELECT (embedding<=>%s)
        cursor.execute("""
            SELECT id, content, embedding<=>%s AS distance FROM documents
            WHERE embedding IS NOT NULL
            ORDER BY embedding<=>%s
            LIMIT 5;""", (query_embedding, query_embedding))
        # OR  ORDER BY distance 
        results = cursor.fetchall()

    for id, content, dist in results:
        print(id, content, dist)