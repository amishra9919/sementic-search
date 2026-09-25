import psycopg
from rank_bm25 import BM25Okapi

def lexical_search(query, top_k=5):

    with psycopg.connect('dbname=sementic_search user=arpit') as conn:
        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT id, document_id, content FROM chunks;""")
            rows = cursor.fetchall()

            # cursor.execute("""
            #     SELECT id, content FROM documents;""")
            # rows = cursor.fetchall()

    chunk_ids = []
    documents = []
    document_ids = []
    for id, document_id, content in rows:
        chunk_ids.append(id)
        documents.append(content)
        document_ids.append(document_id)

    tokenized_documents=[doc.lower().split() for doc in documents]

    bm25 = BM25Okapi(tokenized_documents)
    """
        Documents
            ↓
        Tokenization
            ↓
        BM25 index
    """
    tokenized_query=query.lower().split()
    
    scores = bm25.get_scores(tokenized_query)

    results = []

    for chunk_id, document_id, content, score in zip(chunk_ids,document_ids,documents,scores):
        results.append({
            "id": chunk_id,
            "document_id": document_id,
            "content": content,
            "score": float(score)
        })

        """    
        OR 

        for itr, content in enumerate(documents):
            results.append({
                'id': document_ids[itr],
                'content': documents[itr],
                'score': float(scores[itr]),
            })
        """

    results.sort(
        key=lambda x:x['score'],
        reverse=True
    )

    return results[:top_k]
