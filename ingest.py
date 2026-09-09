import psycopg
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

with psycopg.connect('dbname=sementic_search user=arpit') as conn:
    register_vector(conn)
    with conn.cursor() as cursor:
        cursor.execute("""
                    SELECT id, content FROM documents 
                    WHERE embedding IS NULL;""")
        res = cursor.fetchall()

        for doc_id, content in res:
            embedding = model.encode(content)
            cursor.execute("""
                    UPDATE documents
                    SET embedding = %s
                    WHERE id = %s;
                    """, (embedding, doc_id))
        print("Embeddings added")

