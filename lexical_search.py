import psycopg
from rank_bm25 import BM25Okapi

def lexical_search(query, top_k=5):

    with psycopg.connect('dbname=sementic_search user=arpit') as conn:
        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT id, content FROM documents;""")
            rows = cursor.fetchall()

            # result = lexical_search(rows, query)
            # print(result)

    documents = []
    document_ids = []
    for id, content in rows:
        documents.append(content)
        document_ids.append(id)

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
    for itr, content in enumerate(documents):
        results.append({
            'id': document_ids[itr],
            'content': documents[itr],
            'score': float(scores[itr]),
        })

        """    
        OR 

        for doc_id, content, score in zip(document_ids,documents,scores):
            results.append({
                "id": doc_id,
                "content": content,
                "score": float(score)
            })
        """

    results.sort(
        key=lambda x:x['score'],
        reverse=True
    )

    return results[:top_k]
