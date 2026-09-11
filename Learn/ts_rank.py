import psycopg
from sentence_transformers import SentenceTransformer
from pgvector.psycopg import register_vector

model = SentenceTransformer('all-MiniLM-L6-v2')
query = "python"
with psycopg.connect('dbname=sementic_search user=postgres password=arpitm11814') as conn:
    register_vector(conn)
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, content,ts_rank(
                to_tsvector('english', content),
                plainto_tsquery('english', %s)) AS rank FROM documents
            WHERE to_tsvector('english', content)
                    @@
                  plainto_tsquery('english', %s)
            ORDER BY rank DESC;""",(query, query))
        result = cursor.fetchall()
        print(result)

#---------------------------------------------------------------
#After storing the tsvector in another column
"""
SELECT    id, content,
    ts_rank(
        search_vector,
        plainto_tsquery('english', 'relational database')
    ) AS rank FROM documents
WHERE
    search_vector @@ plainto_tsquery('english', 'relational database')
ORDER BY rank DESC
LIMIT 5;
"""