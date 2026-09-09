import psycopg
from sentence_transformers import SentenceTransformer
from pgvector.psycopg import register_vector

model = SentenceTransformer("all-MiniLM-L6-v2")

query = 'BEST COLORED SHIRT?'
query_embedding = model.encode(query)

with psycopg.connect('dbname=sementic_search user=postgres password=arpitm11814') as conn:
    register_vector(conn)
    with conn.cursor() as cursor:
        cursor.execute("""
                SELECT id, content, embedding<=>%s AS distance from documents
                WHERE embedding IS NOT NULL
                ORDER BY embedding<=>%s;
                """, (query_embedding, query_embedding))
        result = cursor.fetchall()
        for doc_id, content, embedding in result:
            print(doc_id, content, embedding)