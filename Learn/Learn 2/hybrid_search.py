from lexical_search import lexical_search
from vector_search import vector_search
from fusion import reciprocal_rank_fusion
from reranker import rerank

def hybrid_search(
    query, 
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

    final_results = rerank(         #cross-encoder
        query,
        fused_results,
        top_k=final_k
    )
    return final_results

if __name__ == "__main__":

    query = "How can approximate indexing speed up vector search?"

    results = hybrid_search(query)
    print(results)

    for rank, result in enumerate(results, start=1):

        print(f"\nRank: {rank}")
        print(f"Chunk ID: {result['id']}")
        print(f"Document ID: {result['document_id']}")
        print(f"RRF: {result['rrf_score']:.6f}")
        print(
            f"Cross Encoder: "
            f"{result['reranker_score']:.4f}"
        )
        print(result["content"])