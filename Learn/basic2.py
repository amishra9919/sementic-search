import psycopg
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

with psycopg.connect("dbname=sementic_search user=arpit") as conn:
    register_vector(conn) 
    ##we cannot send embedding to the db without register 

    with conn.cursor() as cursor:
        cursor.execute("""SELECT id, content from documents;""")
        rows = cursor.fetchall()
        for doc_id, content in rows:
            embedding = model.encode(content)
            cursor.execute("""UPDATE documents
                                SET embedding = %s 
                                WHERE id = %s""",
                                (embedding, doc_id))
    """For the first document, conceptually:
            embedding → first %s
            doc_id    → second %s

            So PostgreSQL effectively performs:

            UPDATE documents
            SET embedding = <384-dimensional embedding>
            WHERE id = 1;

            Then the loop repeats for document 2.
    """


#-----------------------------------------------------------------------------
#Creating embedding and storing in table 
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
