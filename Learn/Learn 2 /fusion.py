def reciprocal_rank_fusion(bm_results, vector_search, k=60, top_k=5):
    scores = {}
    chunks = {}

    for rank, result in enumerate(bm_results, start=1):
        scores[result['id']] = scores.get(result['id'], 0)
        """OR (ABOVE LINE)
        if doc_id not in rrf_scores:
            rrf_scores[doc_id] = 0
        """
        scores[result['id']] += 1/(k+rank)
        chunks[result['id']] = result

    for rank, result in enumerate(vector_search, start=1):
        scores[result['id']] = scores.get(result['id'], 0)
        scores[result['id']] += 1/(k+rank)
        chunks[result['id']] = result

    ranked = sorted(
        scores.items(),
        key = lambda x:x[1],
        reverse=True
    )

    result = []

    for chunk_id, scores in ranked[:top_k]:
        chunk = chunks[chunk_id]
        result.append({
            'id': chunk_id,
            'document_id': chunk["document_id"],
            'content': chunk['content'],
            'rrf_score': scores
        })

    return result

