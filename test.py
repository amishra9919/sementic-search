<<<<<<< Updated upstream
=======
import psycopg
from sentence_transformers import SentenceTransformer
from pgvector.psycopg import register_vector

def vector_search():
    with psycopg.connect('dbname=sementic_search user=postgres password=arpitm11814') as conn:
        register_vector(conn)
        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT id, content, embedding IS NOT NULL AS has_embedding FROM documents;""")
            result = cursor.fetchall()

            print(result)

vector_search()
>>>>>>> Stashed changes
