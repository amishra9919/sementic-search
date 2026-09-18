from lexical_search import lexical_search
from vector_search import vector_search
from fusion import reciprocal_rank_fusion
from reranker import rerank

def hybrid_search(query, 
    retrieval_k=7, 
    fusion_k=5,
    final_k=3
):
    bm25_results = lexical_search(
        query, 
        retrieval_k
    )

    vector_results = vector_search(
        query, 
        retrieval_k
    )

    fused_results = reciprocal_rank_fusion(
        bm25_results, 
        vector_results,
        fusion_k
    )

    final_results = rerank(
        query,
        fused_results,
        top_k=final_k
    )
    print("fusion results")
    print(final_results)

query = 'computer learning from examples'
hybrid_search(query)
