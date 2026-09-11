import psycopg
from sentence_transformers import SentenceTransformer
from pgvector.psycopg import register_vector

model = SentenceTransformer('all-MiniLM-L6-v2')

query = 'Windows are simpler than Mac'
query_embedding = model.encode(query)

with psycopg.connect('dbname=sementic_search user=arpit') as conn:
    register_vector(conn)
    with conn.cursor() as cursor: 
        cursor.execute("""
            SELECT id, content FROM documents
            WHERE 
                to_tsvector('english', content)
                @@
                plainto_tsquery('english', %s);""", (query,))

        result = cursor.fetchall()
        print("resutl: ", result)