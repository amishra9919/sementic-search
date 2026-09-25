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
                SELECT c.id, c.document_id, c.content, c.embedding<=>%s AS distance FROM chunks AS c
                WHERE c.embedding IS NOT NULL
                ORDER BY distance
                LIMIT %s;""", (query_embedding, top_k))

            rows = cursor.fetchall()

            return [
                {
                    'id': chunk_id,
                    'document_id': document_id,
                    'content': content,
                    'score' : score
                } 
                for chunk_id, document_id, content, score in rows
            ]

            # for chunk_id, document_id, content, distance in rows:
            #     result.append({
            #         'id': chunk_id,
            #         'document_id': document_id,
            #         'content': content,
            #         'distance' : distance
            #     })


            # for doc_id, content, score in rows:
            #     result.append({
            #         'id': doc_id,
            #         'content': content,
            #         'score' : score
            #     })
            
