import psycopg
from sentence_transformers import SentenceTransformer
from pgvector.psycopg import register_vector

modal = SentenceTransformer('all-MiniLM-L6-v2')
##BI-ENCODER ,, have separate encoder
def vector_search(query, top_k=5):
    query_embedding = modal.encode(query)
    result = []
    with psycopg.connect('dbname=sementic_search user=arpit') as conn:
        register_vector(conn)
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, content, embedding<=>%s AS distance FROM documents
                WHERE embedding IS NOT NULL
                ORDER BY distance
                LIMIT %s;""", (query_embedding, top_k))

            rows = cursor.fetchall()

            for doc_id, content, score in rows:
                result.append({
                    'id': doc_id,
                    'content': content,
                    'score' : score
                })

            return result
