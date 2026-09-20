text = """
PostgreSQL is a relational database system.
It supports transactions and SQL queries.
pgvector extends PostgreSQL with vector storage
and similarity search capabilities.
HNSW can be used for approximate nearest
neighbor retrieval over embedding vectors.
"""


chunk = []
chunk_size = 10
overlap = 5
step = chunk_size - overlap
words = text.split()

for i in range(0, len(words), step):
    if i == 0 : overlap_size = 0
    else : overlap_size = overlap
    chunk_words = words[i:i+chunk_size]
    if not chunk_words:
            break
    chunk.append(
            " ".join(chunk_words)
        )
print(chunk)
