def reciprocal_rank_fusion(bm_results, vector_search, k=60, top_k=5):
    scores = {}
    documents = {}

    for rank, result in enumerate(bm_results, start=1):
        scores[result['id']] = scores.get(result['id'], 0)
        """OR (ABOVE LINE)
        if doc_id not in rrf_scores:
            rrf_scores[doc_id] = 0
        """
        scores[result['id']] += 1/(k+rank)
        documents[result['id']] = result['content']

    for rank, result in enumerate(vector_search, start=1):
        scores[result['id']] = scores.get(result['id'], 0)
        scores[result['id']] += 1/(k+rank)
        documents[result['id']] = result['content']

    ranked = sorted(
        scores.items(),
        key = lambda x:x[1],
        reverse=True
    )

    result = []

    for doc_id, scores in ranked[:top_k]:
        result.append({
            'id': doc_id,
            'content': documents[doc_id],
            'rrf_score': scores
        })

    return result

