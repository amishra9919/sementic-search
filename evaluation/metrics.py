def recall_at_k(results, relevant_ids, k):
    retrieved_ids = {
        result["id"]
        for result in results[:k]
    }

    relevant_ids = set(relevant_ids)

    if not relevant_ids:
        return 0.0

    found = retrieved_ids.intersection(relevant_ids)

    return len(found) / len(relevant_ids)


def reciprocal_rank(results, relevant_ids):
    relevant_ids = set(relevant_ids)

    for rank, result in enumerate(results, start=1):
        if result["id"] in relevant_ids:
            return 1 / rank

    return 0.0