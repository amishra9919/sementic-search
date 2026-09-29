import psycopg
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer
from chunking import chunk_text
import hashlib

model = SentenceTransformer('all-MiniLM-L6-v2')

with open('data/sample_document.txt', 'r', encoding="utf-8") as file:
    text = file.read()
    content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest() ## same txt -> same hash

    chunks = chunk_text(text, chunk_size=100, overlap=20)
    embedding = model.encode(chunks, batch_size=32)

    with psycopg.connect('dbname=sementic_search user=postgres password=arpitm11814') as conn:
        register_vector(conn)
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO documents(title, source, content_hash)
                VALUES(%s, %s, %s)
                ON CONFLICT(content_hash) DO NOTHING
                RETURNING id;""", ('PostgreSQL Search Guide', 'sample_document.txt', content_hash))
            ##have created documents_content_hash_idx btree for UNIQUE hash so it will throw err for dup hash .. to prevent --> on conflict used
            result = cursor.fetchone()
            if result:
                document_id = result[0]
                for chunk_index, (chunks, embedding) in enumerate(zip(chunks, embedding)):
                    cursor.execute("""
                        INSERT INTO chunks(document_id, chunk_index, embedding, content)
                        VALUES (%s, %s, %s, %s);""", (document_id, chunk_index, embedding, chunks))
                print(f"INSERTED INTO DOCUMENT {document_id} "
                        f"WITH {len(chunks)} chunks")
            else:
                print("Document Already Exist")
        


    
############################################################################################

# #Right now it ingest the embeddings of content in the rows BELOW

# with psycopg.connect('dbname=sementic_search user=postgres password=arpitm11814') as conn:
#     register_vector(conn)
#     with conn.cursor() as cursor:
#         cursor.execute("""
#                     SELECT id, content FROM documents 
#                     WHERE embedding IS NULL;""")
#         res = cursor.fetchall()

#         for doc_id, content in res:
#             embedding = model.encode(content)
#             cursor.execute("""
#                     UPDATE documents
#                     SET embedding = %s
#                     WHERE id = %s;
#                     """, (embedding, doc_id))
#         print(f"Embedded document res")


