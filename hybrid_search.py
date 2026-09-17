from lexical_search import lexical_search
from vector_search import vector_search
from fusion import reciprocal_rank_fusion

query = 'computer learning from examples'

bm25_results = lexical_search(
    query, top_k=5
)

vector_results = vector_search(
    query, top_k=5
)

rrf = reciprocal_rank_fusion(
    bm25_results, vector_results
)
print(len(rrf), len(vector_results), len(bm25_results))
# print('Rank wise result')
# print('Doc_ID       Content      RRF SCORE')
# for itr, (doc_id, score) in enumerate(rrf):
#     print(doc_id, vector_results[itr]['content'], score)