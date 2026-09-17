def reciprocal_rank_fusion(bm_results, vector_search):
    scores = {}
    k = 60

    for rank, result in enumerate(bm_results, start=1):
        scores[result['id']] = scores.get(result['id'], 0)
        """OR (ABOVE LINE)
        if doc_id not in rrf_scores:
            rrf_scores[doc_id] = 0
        """
        scores[result['id']] += 1/(k+rank)

    for rank, result in enumerate(vector_search, start=1):
        scores[result['id']] = scores.get(result['id'], 0)
        scores[result['id']] += 1/(k+rank)

    ranked = sorted(
        scores.items(),
        key = lambda x:x[1],
        reverse=True
    )

    return ranked

