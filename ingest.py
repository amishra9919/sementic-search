"""
A b-tree created on hash as unique in parent table... NOT SEPARATE INDEX
"""


import psycopg
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer
from chunking import chunk_text
from database import pool
from pathlib import Path
import hashlib
import os

model = SentenceTransformer('all-MiniLM-L6-v2')
DB_CONNECTION = ('host=localhost port=5433 dbname=sementic_search user=postgres password=postgres')

def ingest_directory(directory):
    paths = Path(directory).glob("*.txt")
    print(paths)
    for path in paths:
        ingest_document(path)
def ingest_document(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        text = file.read()
        content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest() ## same txt -> same hash

        title = os.path.basename(file_path)

        # ingest_directory('evaluation/corpus')
        
        with pool.connection() as conn:
            register_vector(conn)
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO documents(title, source, content_hash)
                    VALUES(%s, %s, %s)
                    ON CONFLICT(content_hash) DO NOTHING
                    RETURNING id;""", (title, file_path, content_hash))
                ##have created documents_content_hash_idx btree for UNIQUE hash so it will throw err for dup hash .. to prevent --> on conflict used
                result = cursor.fetchone()

                chunks = chunk_text(text, chunk_size=100, overlap=20)
                embedding = model.encode(chunks, batch_size=32)
                
                if result is None:
                    print(
                        f"Skipping existing document: "
                        f"{file_path}")
                    return
                
                document_id = result[0]
                chunk_rows = []

                for chunk_index, (chunk, embedding) in enumerate(zip(chunks, embedding)):
                    chunk_rows.append((
                        document_id,
                        chunk_index,
                        chunk,
                        embedding
                    ))

                cursor.executemany("""
                    INSERT INTO chunks(document_id, chunk_index, content, embedding)
                    VALUES (%s, %s, %s, %s);""", chunk_rows)
                
        print(f"INSERTED INTO DOCUMENT {document_id} "
                f"WITH {len(chunks)} chunks")
        