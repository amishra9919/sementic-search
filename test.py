import psycopg
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder

modal = SentenceTransformer('all-MiniLM-L6-v2')
query = 'playing'
model_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L6-v2')
def vsearch(query, top_k=10):
    query_embedding = modal.encode(query)

    with psycopg.connect('dbname=sementic_search user=arpit') as conn:
        register_vector(conn)
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, content, embedding<=>%s as distance FROM documents
                WHERE embedding IS NOT NULL
                ORDER BY distance
                LIMIT %s""", (query_embedding, top_k))
            rows = cursor.fetchall()

            result = []

            for id, content, score in rows:
                result.append({
                    'id':id,
                    'content':content,
                    'score':score
                })
            return result

def search(query, top_k=10):
    with psycopg.connect('dbname=sementic_search user=arpit') as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, content FROM documents;""")
            rows = cursor.fetchall()

    document_id = []
    document = []
    for doc_id, content in rows:
        document.append(content)
        document_id.append(doc_id)

    tokenized_doc = [doc.lower().split() for doc in document]
    bm_result = BM25Okapi(tokenized_doc)

    tokenized_query = query.lower().split()

    score = bm_result.get_scores(tokenized_query)

    result = []

    for content, doc_id, score in zip(document, document_id, score):
        result.append({
            'id': doc_id,
            'content': content, 
            'score': float(score)
        })

    result.sort(
        key=lambda x:x['score'],
        reverse=True
    )

    return result[:top_k]

def rrf(vecSer, keySer, top_k=8, rrf_threshold=60):
    scores = {}
    document = {}

    for rank, row in enumerate(vecSer):
        document[row['id']] = row['content']
        rrf_score = 1/(rrf_threshold+rank)
        scores[row['id']] = scores.get(row['id'], 0)
        scores[row['id']] += rrf_score

    for rank, row in enumerate(keySer):
        document[row['id']] = row['content']
        rrf_score = 1/(rrf_threshold+rank)
        scores[row['id']] = scores.get(row['id'], 0)
        scores[row['id']] += rrf_score

    rrf_rank = sorted(
        scores.items(),
        key=lambda x:x[1],
        reverse=True
    )

    rrf_result = []

    for id, score in rrf_rank[:top_k]:
        rrf_result.append({
            'id':id,
            'content':document[id],
            'score':score
        })

    return rrf_result

def rerank(query, fused_results, top_k=5):

    pair = [(doc['content'], query) for doc in fused_results]
    scores = model_encoder.predict(pair)

    rerank_result = []

    for row, score in zip(fused_results, scores):
        rerank_result.append({
            **row,
            'score:': float(score)
        })
    
    return rerank_result

vecSer = vsearch(query, 10)
keySer = search(query, 10)
fusion = rrf(vecSer, keySer, top_k=8, rrf_threshold=60)
rerank = rerank(query, fusion, top_k=5)

print(rerank)