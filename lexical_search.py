import psycopg
from rank_bm25 import BM25Okapi

def bm25_search(rows, top_k = 5):
    document_ids = []
    document = []

    for id, content in rows:
        document_ids.append(id)
        document.append(content)

    tokenized_docs = [doc.lower().split() for doc in document]

    bm25 = BM25Okapi(tokenized_docs)

    """
        Documents
            ↓
        Tokenization
            ↓
        BM25 index
    """

    query = 'Machine Learining'
    tokenized_query = query.lower().split()

    scores = bm25.get_scores(tokenized_query)

    # def ret(the_tuple):
    #     return the_tuple[2]

    rank = sorted(
        zip(document_ids, document, scores),
        key=lambda x: x[2],
        # key=ret, #only if ret is defined (just for understanding)
        reverse=True
    )
    top_krows = rank[:top_k]

    return top_krows

with psycopg.connect("dbname=sementic_search user=arpit") as conn:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, content FROM documents
            ORDER by id;""")

        rows = cur.fetchall()

    top_k = bm25_search(rows, 5)

    for doc_id, content, score in top_k:
        print(doc_id, content, score)
    # print("document: ", rank)
