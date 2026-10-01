import json

from lexical_search import lexical_search
from vector_search import vector_search
# from hybrid_search import (
#     hybrid_retrieval,
#     hybrid_search
# )

from evaluation.metrics import (
    recall_at_k,
    reciprocal_rank
)

with open("evaluation/queries.json","r",encoding="utf-8") as file:
    queries = json.load(file)

def evaluate_method(
    name,
    search_function,
    queries,
    k=5
):

    recalls = []
    reciprocal_ranks = []

    for item in queries:

        results = search_function(
            item["query"]
        )

        relevant_ids = item[
            "relevant_chunk_ids"
        ]

        recalls.append(
            recall_at_k(
                results,
                relevant_ids,
                k
            )
        )

        reciprocal_ranks.append(
            reciprocal_rank(
                results,
                relevant_ids
            )
        )

    return {
        "method": name,
        "recall_at_k": (
            sum(recalls) / len(recalls)
        ),
        "mrr": (
            sum(reciprocal_ranks)
            / len(reciprocal_ranks)
        )
    }

bm25_metrics = evaluate_method(
    "BM25",
    lambda query: lexical_search(
        query,
        top_k=5
    ),
    queries
)

vector_metrics = evaluate_method(
    "Vector",
    lambda query: vector_search(
        query,
        top_k=5
    ),
    queries
)

print(bm25_metrics)
print(vector_metrics)

# hybrid_search(
#     query,
#     retrieval_k=50,
#     fusion_k=20,
#     final_k=5
# )