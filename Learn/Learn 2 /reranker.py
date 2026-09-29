from sentence_transformers import CrossEncoder

model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L6-v2')

def rerank(query,candidates,top_k=3):

    pairs = [[query, doc['content']] for doc in candidates]

    scores = model.predict(pairs)

    results = []

    for candidate, score in zip(candidates, scores):
        results.append({
            **candidate, 
            "reranker_score": float(score)
        })

    results.sort(
        key=lambda x:x['reranker_score'],
        reverse=True
    )

    return results

