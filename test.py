import psycopg
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer

modal = SentenceTransformer('all-MiniLM-L6-v2')
query = 'Postgr SL akdhsfklaudg'
query_embedding = modal.encode(query)

with psycopg.connect('dbname=sementic_search user=postgres password=arpitm11814') as conn:
    register_vector(conn)
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, content, embedding<=>%s as distance FROM documents
            WHERE embedding IS NOT NULL
            ORDER BY distance;""", (query_embedding, ))
        rows = cursor.fetchall()

        print(rows)

